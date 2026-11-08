import os
import json
import stripe
import urllib.request
from http.server import BaseHTTPRequestHandler

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
SUPPORT_EMAIL = "dannydth87@gmail.com"

FILE_CATALOG = {
    "flash_bot": {
        "title": "NQ Fair Value Gap Sniper & Trailing Drawdown ATM Guard",
        "zip_url": "https://thefundedbible.com/downloads/NQ_FVG_Sniper_NT8.zip",
        "instructions": "Import via Tools -> Import -> NinjaScript Add-On in NinjaTrader 8."
    },
    "master_bundle": {
        "title": "Master Algo Bundle (All Indicators, Killzones & 20 ATM Templates)",
        "zip_url": "https://thefundedbible.com/downloads/Master_Algo_Bundle_NT8.zip",
        "instructions": "Extract and import indicators. Copy ATM presets to Documents/NinjaTrader 8/templates/AtmStrategy/."
    },
    "autotrader_suite": {
        "title": "Autotrader Execution Suite (Full Hands-Free C# Strategies)",
        "zip_url": "https://thefundedbible.com/downloads/Autotrader_Execution_Suite_NT8.zip",
        "instructions": "Import strategies via NinjaScript Add-On and enable auto strategy execution."
    },
    "vip_mastermind": {
        "title": "VIP Prop Desk Mastermind (Full Uncompiled Source Code + Setup)",
        "zip_url": "https://thefundedbible.com/downloads/VIP_Institutional_Vault_Source.zip",
        "instructions": "Download source archive. Reply to this email to book 1-on-1 deployment."
    }
}

def send_delivery_email(recipient_email, pkg):
    if not RESEND_API_KEY:
        print(f"[MOCK] Delivery prepared for: {recipient_email}")
        return
    try:
        html = f"""<div style="font-family:sans-serif;background:#030508;color:#f1f5f9;padding:30px;">
            <h2>Your Download: {pkg['title']}</h2>
            <p><a href="{pkg['zip_url']}" style="background:#00ff9d;color:#000;padding:12px 24px;text-decoration:none;font-weight:bold;border-radius:6px;display:inline-block;">Download .ZIP File</a></p>
            <p>{pkg['instructions']}</p>
            <p style="color:#64748b;font-size:12px;">Support: {SUPPORT_EMAIL}</p>
        </div>"""
        data = json.dumps({
            "from": "The Funded Bible <deliveries@thefundedbible.com>",
            "to": [recipient_email],
            "subject": f"Download: {pkg['title']}",
            "html": html
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.resend.com/emails",
            data=data,
            headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        sig = self.headers.get("Stripe-Signature", "")
        try:
            if WEBHOOK_SECRET:
                event = stripe.Webhook.construct_event(body, sig, WEBHOOK_SECRET)
            else:
                event = json.loads(body.decode("utf-8"))

            if event.get("type") == "checkout.session.completed":
                s = event["data"]["object"]
                email = s.get("customer_details", {}).get("email")
                amt = s.get("amount_total", 0)
                slug = s.get("metadata", {}).get("slug", "")

                if amt == 900 or "fvg" in slug or "drawdown" in slug:
                    p = FILE_CATALOG["flash_bot"]
                elif amt == 29900 or "silver" in slug:
                    p = FILE_CATALOG["autotrader_suite"]
                elif amt == 49900 or "mastermind" in slug:
                    p = FILE_CATALOG["vip_mastermind"]
                else:
                    p = FILE_CATALOG["master_bundle"]

                if email:
                    send_delivery_email(email, p)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"received":true}')
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e).encode("utf-8"))