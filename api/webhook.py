import os
import json
import stripe
from http.server import BaseHTTPRequestHandler

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        payload = self.rfile.read(content_length)
        sig_header = self.headers.get("Stripe-Signature", "")

        try:
            if WEBHOOK_SECRET:
                event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
            else:
                event = json.loads(payload.decode("utf-8"))

            if event.get("type") == "checkout.session.completed":
                session = event["data"]["object"]
                customer_email = session.get("customer_details", {}).get("email")
                print(f"[PAID] Delivered automated bot file access to: {customer_email}")

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"received": True}).encode("utf-8"))
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))
