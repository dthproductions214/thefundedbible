# -*- coding: utf-8 -*-
import sys
import io
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BOT_TOKEN = "9042945272:AAGVY4bd68LCk3YIV8B0OUEIKmt0UKGweJ8"
CHAT_ID = "8585819972"

def send_signal(asset_name, price, change_pct, low, high):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    message = (
        f"🚨 HIGH-ALERT 🚨 🚀 BULLISH BREAKOUT - INSTANT BUY PRESSURE\n"
        f"📊 Asset: {asset_name}\n"
        f"💰 Trade Price: {price} ({change_pct} in 15m)\n"
        f"📈 Session Extreme: {low} - {high}\n"
        f"🎯 Tactical Play: Trailing drawdown is a target. Adjust risk now.\n\n"
        f"🔥 PASS YOUR PROP EVALUATION - NO MERCY.\n"
        f"⚡ Grab the High-Volatility ATM Risk Setups & Playbooks NOW:\n"
        f"👉 https://thefundedbible.com\n"
        f"💎 USE CODE BIBLE80 AT CHECKOUT FOR 80% OFF - SECURE THE BAG."
    )

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        if data.get("ok"):
            print(f"[SUCCESS] Signal sent for {asset_name}!")
        else:
            print(f"[ERROR] Telegram API failed: {data}")
    except Exception as e:
        print(f"[EXCEPTION] Connection error: {e}")

if __name__ == "__main__":
    print("Initializing The Funded Bible Signal Bot...")
    send_signal("Gold (GC)", "4,079.50", "+0.13%", "4,035.10", "4,090.70")
