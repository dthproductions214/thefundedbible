# -*- coding: utf-8 -*-
import os, time, json, urllib.request
import yfinance as yf

TELEGRAM_BOT_TOKEN = "9042945272:AAGVY4bd68LCK3YIV8B0OUEIKmt0UKGweJ8"
TELEGRAM_CHAT_ID = "8585819972"
STATE_FILE = "state.json"

PROMO_FOOTER = "\n\nPass Your Prop Evaluation:\nhttps://thefundedbible.com (Code BIBLE80)"

try:
    with open(STATE_FILE, "r") as f:
        seen = json.load(f)
except:
    seen = {}

now = time.time()
seen = {k: v for k, v in seen.items() if now - v < 7200}

def send_alert(msg):
    if not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print("Telegram Error:", e)

def check_market():
    tickers = ["NQ=F", "ES=F", "CL=F", "GC=F"]
    for t in tickers:
        try:
            df = yf.Ticker(t).history(period="1d", interval="1m")
            if df.empty or len(df) < 5:
                continue

            latest = df.iloc[-1]
            close = latest['Close']
            open_p = latest['Open']

            move_pct = abs(close - open_p) / open_p * 100
            if move_pct > 0.3:
                key = f"{t}_move_{df.index[-1]}"
                if key not in seen:
                    direction = "SURGE UP" if close > open_p else "CRASH DOWN"
                    msg = f"TFB CLOUD RADAR\n\nInstrument: {t}\nMove: {direction} ({move_pct:.2f}% in 1m)\nPrice: {close:.2f}{PROMO_FOOTER}"
                    send_alert(msg)
                    seen[key] = now

        except Exception as e:
            print(f"Error checking {t}:", e)

    with open(STATE_FILE, "w") as f:
        json.dump(seen, f)

if __name__ == "__main__":
    print("Cloud Engine Running...")
    check_market()
    print("Check complete.")
