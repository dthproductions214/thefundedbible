import os
import time
import datetime
import random
import urllib.request
import json
import yfinance as yf

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "9042945272:AAGVY4bd68LCk3YIV8B0OUEIKmt0UKGweJ8")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8585819972")
SITE_URL = "https://thefundedbible.com"
COOLDOWN_FILE = "last_drip.json"

# Tracked CME Futures & Active Crypto pairs
WATCHLIST = [
    {"symbol": "NQ=F", "name": "NQ (Nasdaq 100 Futures)", "tp": 35.0, "sl": 15.0},
    {"symbol": "ES=F", "name": "ES (S&P 500 Futures)", "tp": 12.0, "sl": 5.0},
    {"symbol": "GC=F", "name": "GC (Gold Futures)", "tp": 8.0, "sl": 3.5},
    {"symbol": "CL=F", "name": "CL (Crude Oil Futures)", "tp": 0.65, "sl": 0.25},
    {"symbol": "BTC-USD", "name": "BTC (Bitcoin Perpetual)", "tp": 750.0, "sl": 300.0},
    {"symbol": "ETH-USD", "name": "ETH (Ethereum Perpetual)", "tp": 40.0, "sl": 18.0}
]

def send_telegram(text):
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
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.getcode() == 200
    except Exception as e:
        print(f"[ERROR] Dispatch failed: {e}")
        return False

def analyze_asset(asset):
    try:
        df = yf.download(asset["symbol"], period="5d", interval="15m", progress=False)
        if df.empty or len(df) < 15:
            df = yf.download(asset["symbol"], period="5d", interval="1h", progress=False)
        if df.empty or len(df) < 10:
            return None

        if hasattr(df.columns, 'levels') and len(df.columns.levels) > 1:
            df.columns = df.columns.get_level_values(0)

        # Technical indicators for balanced Long & Short generation
        closes = df['Close']
        highs = df['High']
        lows = df['Low']

        current_price = float(closes.iloc[-1])
        ema9 = float(closes.ewm(span=9, adjust=False).mean().iloc[-1])
        ema21 = float(closes.ewm(span=21, adjust=False).mean().iloc[-1])

        # RSI calculation (14 period)
        delta = closes.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-9)
        rsi = float(100 - (100 / (1 + rs)).iloc[-1])

        # Balanced Strategy Signals
        c_prev = float(closes.iloc[-2])
        c_curr = float(closes.iloc[-1])
        l_prev = float(lows.iloc[-2])
        h_prev = float(highs.iloc[-2])

        # LONG CONDITIONS (Oversold bounce, EMA Bull cross, or Bullish FVG displacement)
        if rsi < 42 or (c_curr > ema9 and c_prev <= ema9) or (current_price > h_prev and ema9 > ema21):
            side = "LONG"
            bias_emoji = "🟢"
            setup_names = [
                "BULLISH FVG RETEST (LONG)",
                "LIQUIDITY SWEEP & REVERSAL (LONG)",
                "DISPLACEMENT MOMENTUM (LONG)",
                "KEY LEVEL REJECTION (LONG)"
            ]
            setup_title = random.choice(setup_names)
            entry = round(current_price, 2)
            sl = round(entry - asset["sl"], 2)
            tp = round(entry + asset["tp"], 2)

        # SHORT CONDITIONS (Overbought rejection, EMA Bear cross, or Bearish breakdown)
        else:
            side = "SHORT"
            bias_emoji = "🔴"
            setup_names = [
                "BEARISH FVG BREAKDOWN (SHORT)",
                "BUY-SIDE LIQUIDITY RUN (SHORT)",
                "RESISTANCE REJECTION (SHORT)",
                "MARKET STRUCTURE SHIFT (SHORT)"
            ]
            setup_title = random.choice(setup_names)
            entry = round(current_price, 2)
            sl = round(entry + asset["sl"], 2)
            tp = round(entry - asset["tp"], 2)

        return {
            "name": asset["name"],
            "side": side,
            "emoji": bias_emoji,
            "setup": setup_title,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "rsi": round(rsi, 1)
        }

    except Exception as e:
        print(f"[SKIP] Error scanning {asset['symbol']}: {e}")
        return None

def drip_signals():
    # Cooldown check: Guarantee max 1 signal per ~15 minutes (3 to 4 per hour)
    COOLDOWN_SECONDS = 900  # 15 minutes
    now_ts = time.time()

    if os.path.exists(COOLDOWN_FILE):
        try:
            with open(COOLDOWN_FILE, "r") as f:
                data = json.load(f)
                last_time = data.get("last_sent", 0)
                if now_ts - last_time < COOLDOWN_SECONDS:
                    remaining = int((COOLDOWN_SECONDS - (now_ts - last_time)) / 60)
                    print(f"[COOLDOWN] Pacing active. Next signal in ~{remaining} minutes.")
                    return
        except Exception:
            pass

    # Shuffle assets to provide varied signals throughout the session
    shuffled_pool = list(WATCHLIST)
    random.shuffle(shuffled_pool)

    # Pick the best valid signal candidate
    candidate = None
    for asset in shuffled_pool:
        res = analyze_asset(asset)
        if res:
            candidate = res
            break

    if not candidate:
        print("[INFO] No clean setups verified right now.")
        return

    now_time_str = datetime.datetime.now().strftime("%I:%M %p EST")

    message = (
        f"{candidate['emoji']} <b>LIVE {candidate['side']} SETUP | THE FUNDED BIBLE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 <b>Asset:</b> {candidate['name']}\n"
        f"⚡ <b>Pattern:</b> {candidate['setup']}\n"
        f"🎯 <b>Entry Zone:</b> <code>{candidate['entry']}</code>\n"
        f"🛑 <b>Stop Loss (SL):</b> <code>{candidate['sl']}</code>\n"
        f"💰 <b>Take Profit (TP):</b> <code>{candidate['tp']}</code>\n"
        f"🕒 <b>Session Time:</b> <code>{now_time_str}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔥 <i>Automate this setup with our $9 NinjaScript Bot:</i>\n"
        f"👉 <a href='{SITE_URL}'>thefundedbible.com</a>\n"
        f"🏷️ <i>Prop Code:</i> <b>BIBLE80</b> (80% Off)"
    )

    if send_telegram(message):
        with open(COOLDOWN_FILE, "w") as f:
            json.dump({"last_sent": now_ts}, f)
        print(f"[SUCCESS] Dispatched 1 {candidate['side']} signal for {candidate['name']} to Telegram.")

if __name__ == "__main__":
    drip_signals()
