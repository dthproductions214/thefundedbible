import os
import time
import datetime
import urllib.request
import urllib.parse
import json
import yfinance as yf

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "9042945272:AAGVY4bd68LCk3YIV8B0OUEIKmt0UKGweJ8")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8585819972")
SITE_URL = "https://thefundedbible.com"
STATE_FILE = "last_signals.json"

# Full 24/7 asset tracking: CME Globex Futures + 24/7 Crypto Futures
ASSETS = {
    "NQ=F": {"name": "NQ (Nasdaq 100 Futures)", "tp_pts": 35.0, "sl_pts": 15.0, "type": "cme"},
    "ES=F": {"name": "ES (S&P 500 Futures)", "tp_pts": 12.0, "sl_pts": 5.0, "type": "cme"},
    "GC=F": {"name": "GC (Gold Futures)", "tp_pts": 8.0, "sl_pts": 3.5, "type": "cme"},
    "CL=F": {"name": "CL (Crude Oil Futures)", "tp_pts": 0.65, "sl_pts": 0.25, "type": "cme"},
    "BTC-USD": {"name": "BTC (Bitcoin Perpetual)", "tp_pts": 650.0, "sl_pts": 280.0, "type": "crypto"},
    "ETH-USD": {"name": "ETH (Ethereum Perpetual)", "tp_pts": 35.0, "sl_pts": 18.0, "type": "crypto"}
}

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception:
        pass

def send_telegram_alert(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.getcode() == 200
    except Exception as e:
        print(f"[ERROR] Telegram transmission failed: {e}")
        return False

def scan_live_feeds():
    state = load_state()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S EST")
    print(f"[{now_str}] Polling live market telemetry...")

    dispatched = 0
    for ticker, info in ASSETS.items():
        try:
            df = yf.download(ticker, period="5d", interval="15m", progress=False)
            if df.empty or len(df) < 5:
                df = yf.download(ticker, period="5d", interval="1h", progress=False)

            if df.empty or len(df) < 3:
                continue

            if hasattr(df.columns, 'levels') and len(df.columns.levels) > 1:
                df.columns = df.columns.get_level_values(0)

            c1 = df.iloc[-3]
            c2 = df.iloc[-2]
            c3 = df.iloc[-1]

            candle_time = str(df.index[-1])
            current_price = float(c3['Close'])

            # Deduplication: Avoid duplicate broadcasts on identical candle timestamps and pricing
            last_recorded = state.get(ticker, {})
            if last_recorded.get("time") == candle_time and last_recorded.get("price") == current_price:
                continue

            if float(c3['Low']) > float(c1['High']) and float(c2['Close']) > float(c2['Open']):
                setup_title = "BULLISH FVG EXPANSION (LONG)"
                bias_color = "🟢"
                entry = round(current_price, 2)
                sl = round(entry - info['sl_pts'], 2)
                tp = round(entry + info['tp_pts'], 2)
            elif float(c3['High']) < float(c1['Low']) and float(c2['Close']) < float(c2['Open']):
                setup_title = "BEARISH FVG BREAKDOWN (SHORT)"
                bias_color = "🔴"
                entry = round(current_price, 2)
                sl = round(entry + info['sl_pts'], 2)
                tp = round(entry - info['tp_pts'], 2)
            else:
                ema_fast = df['Close'].rolling(window=5).mean().iloc[-1]
                ema_slow = df['Close'].rolling(window=13).mean().iloc[-1]
                if ema_fast >= ema_slow:
                    setup_title = "ORDERFLOW MOMENTUM LONG"
                    bias_color = "🟢"
                    entry = round(current_price, 2)
                    sl = round(entry - info['sl_pts'], 2)
                    tp = round(entry + info['tp_pts'], 2)
                else:
                    setup_title = "LIQUIDITY RUN SHORT"
                    bias_color = "🔴"
                    entry = round(current_price, 2)
                    sl = round(entry + info['sl_pts'], 2)
                    tp = round(entry - info['tp_pts'], 2)

            message = (
                f"{bias_color} <b>LIVE DISPLACEMENT SETUP | THE FUNDED BIBLE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📊 <b>Asset:</b> {info['name']}\n"
                f"⚡ <b>Action:</b> {setup_title}\n"
                f"🎯 <b>Live Zone:</b> <code>{entry}</code>\n"
                f"🛑 <b>Hard Stop (SL):</b> <code>{sl}</code>\n"
                f"💰 <b>Take Profit (TP):</b> <code>{tp}</code>\n"
                f"⏱️ <b>Print Time:</b> <code>{now_str}</code>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🔥 <i>Automate with our $9 NinjaScript Bot:</i>\n"
                f"👉 <a href='{SITE_URL}'>thefundedbible.com</a>\n"
                f"🏷️ <i>Prop Code:</i> <b>BIBLE80</b>"
            )

            if send_telegram_alert(message):
                state[ticker] = {"time": candle_time, "price": current_price}
                save_state(state)
                dispatched += 1
                time.sleep(2)

        except Exception as e:
            print(f"[ERROR] Processing {ticker}: {e}")

    print(f"[COMPLETE] {dispatched} new signals pushed to Telegram.")

if __name__ == "__main__":
    scan_live_feeds()
