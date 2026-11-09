import os
import json
from http.server import BaseHTTPRequestHandler
import stripe

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("content-length", 0))
        post_data = self.rfile.read(content_length)
        payload = post_data.decode("utf-8") if post_data else ""
        sig_header = self.headers.get("stripe-signature")

        event = None

        # 1. Allow health-checks and test pings without failing
        try:
            body_json = json.loads(payload) if payload else {}
            if body_json.get("type") == "test_ping":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "online",
                    "message": "Webhook endpoint is operational",
                    "env_stripe_key_present": bool(stripe.api_key),
                    "env_webhook_secret_present": bool(endpoint_secret)
                }).encode("utf-8"))
                return
        except Exception:
            pass

        # 2. Stripe Event Verification
        if endpoint_secret and sig_header:
            try:
                event = stripe.Webhook.construct_event(
                    payload, sig_header, endpoint_secret
                )
            except ValueError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid payload")
                return
            except stripe.error.SignatureVerificationError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid signature")
                return
        else:
            # Fallback parsing if signature header is absent or during manual testing
            try:
                event = json.loads(payload)
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f"Payload parse error: {str(e)}".encode("utf-8"))
                return

        # 3. Handle successful checkout sessions
        event_type = event.get("type") if isinstance(event, dict) else getattr(event, "type", "")
        if event_type == "checkout.session.completed":
            session = event.get("data", {}).get("object", {}) if isinstance(event, dict) else event.data.object
            customer_email = session.get("customer_details", {}).get("email") or session.get("customer_email")
            # Logic for automated fulfillment / email notification can execute here
            print(f"[FULFILLMENT] Order completed for: {customer_email}")

        # Always return 200 to Stripe
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"received": True}).encode("utf-8"))

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "online",
            "endpoint": "https://www.thefundedbible.com/api/webhook"
        }).encode("utf-8"))