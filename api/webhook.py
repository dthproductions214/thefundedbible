import os
import json
import stripe
from http.server import BaseHTTPRequestHandler
import urllib.request

# Read secret keys strictly from environment variables to pass GitHub secret scanning
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
SUPPORT_EMAIL = "dannydth87@gmail.com"

# Direct Cloud/CDN Download Targets for NinjaTrader 8 .zip packages
FILE_CATALOG = {
    "flash_bot": {
        "title": "NQ Fair Value Gap Sniper & Trailing Drawdown ATM Guard",
        "zip_url": "https://thefundedbible.com/downloads/NQ_FVG_Sniper_NT8.zip",
        "instructions": (
            "1. Open NinjaTrader 8.<br/>"
            "2. Go to <b>Tools -> Import -> NinjaScript Add-On</b>.<br/>"
            "3. Select the downloaded <code>NQ_FVG_Sniper_NT8.zip</code> file.<br/>"
            "4. Copy the included <code>.xml</code> ATM presets into your <code>Documents/NinjaTrader 8/templates/AtmStrategy/</code> folder."
        )
    },
    "master_bundle": {
        "title": "Master Algo Bundle (All Indicators, Killzones & 20 ATM Templates)",
        "zip_url": "https://thefundedbible.com/downloads/Master_Algo_Bundle_NT8.zip",
        "instructions": (
            "1. Extract the bundle folder.<br/>"
            "2. Import the indicators via <b>Tools -> Import -> NinjaScript Add-On</b>.<br/>"
            "3. Drop the 20 ATM XML templates into <code>Documents/NinjaTrader 8/templates/AtmStrategy/</code>."
        )
    },
    "autotrader_suite": {
        "title": "Autotrader Execution Suite (Full Hands-Free C# Strategies)",
        "zip_url": "https://thefundedbible.com/downloads/Autotrader_Execution_Suite_NT8.zip",
        "instructions": (
            "1. Import the automated strategies via <b>Tools -> Import -> NinjaScript Add-On</b>.<br/>"
            "2. Ensure automated strategy execution is toggled ON in NinjaTrader 8 chart strategies window."
        )
    },
    "vip_mastermind": {
        "title": "VIP Prop Desk Mastermind (Full Uncompiled Source Code + Setup)",
        "zip_url": "https://thefundedbible.com/downloads/VIP_Institutional_Vault_Source.zip",
        "instructions": (
            "1. Download your full uncompiled C# source vault.<br/>"
            "2. Reply directly to this email to confirm your 1-on-1 desk setup session."
        )
    }
}

def send_delivery_email(recipient_email, package_info):
    subject = f"Your NinjaTrader 8 Download: {package_info['title']} | The Funded Bible"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="background-color: #030508; color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 32px; margin: 0;">
        <div style="max-width: 600px; margin: 0 auto; background: #080c14; border: 1px solid rgba(0, 242, 254, 0.25); border-radius: 16px; padding: 32px;">
            <div style="font-size: 11px; font-weight: 700; color: #00ff9d; letter-spacing: 1.5px; text-transform: uppercase;">Payment Confirmed // Instant Delivery</div>
            <h1 style="color: #ffffff; font-size: 22px; margin: 12px 0 20px 0;">{package_info['title']}</h1>
            
            <p style="color: #94a3b8; font-size: 14px; line-height: 1.6;">
                Your order has processed successfully. Click the button below to download your NinjaTrader 8 package directly:
            </p>

            <div style="margin: 28px 0; text-align: center;">
                <a href="{package_info['zip_url']}" style="background: linear-gradient(90deg, #00f2fe, #00ff9d); color: #000000; font-weight: 800; font-size: 15px; padding: 14px 28px; border-radius: 10px; text-decoration: none; display: inline-block;">
                    Download NinjaTrader 8 .ZIP &rarr;
                </a>
            </div>

            <div style="background: #04070b; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 10px; padding: 20px; margin-bottom: 24px;">
                <div style="color: #00f2fe; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">Installation Steps:</div>
                <div style="color: #cbd5e1; font-size: 13px; line-height: 1.6;">{package_info['instructions']}</div>
            </div>

            <hr style="border: 0; border-top: 1px solid rgba(255, 255, 255, 0.1); margin: 24px 0;">
            <p style="color: #64748b; font-size: 12px; margin: 0;">
                Questions or setup issues? Contact desk support at <a href="mailto:{SUPPORT_EMAIL}" style="color: #00f2fe;">{SUPPORT_EMAIL}</a>.
            </p>
        </div>
    </body>
    </html>
    """

    if RESEND_API_KEY:
        try:
            payload = {
                "from": "The Funded Bible <deliveries@thefundedbible.com>",
                "to": [recipient_email],
                "subject": subject,
                "html": html_content
            }
            req = urllib.request.Request(
                "https://api.resend.com/emails",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {RESEND_API_KEY}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                print(f"[RESEND SUCCESS] Delivered download email to: {recipient_email}")
        except Exception as e:
            print(f"[RESEND ERROR] Failed sending to {recipient_email}: {e}")
    else:
        print(f"[SIMULATION] Resend key not set. Email queued for: {recipient_email}")

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
                amount = session.get("amount_total", 0)
                metadata = session.get("metadata", {})
                slug = metadata.get("slug", "")

                if amount == 900 or "fvg-sniper" in slug or "drawdown" in slug:
                    pkg = FILE_CATALOG["flash_bot"]
                elif amount == 29900 or "silver-bullet" in slug:
                    pkg = FILE_CATALOG["autotrader_suite"]
                elif amount == 49900 or "mastermind" in slug:
                    pkg = FILE_CATALOG["vip_mastermind"]
                else:
                    pkg = FILE_CATALOG["master_bundle"]

                if customer_email:
                    send_delivery_email(customer_email, pkg)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"received": True}).encode("utf-8"))

        except Exception as e:
            print(f"[WEBHOOK FAULT] {e}")
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))
