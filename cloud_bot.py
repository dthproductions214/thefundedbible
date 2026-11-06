import os, time, json, urllib.request
import yfinance as yf

TELEGRAM_BOT_TOKEN = "9042945272:AAGVY4bd68LCk3YIV8B0OUEIKmt0UKGweJ8"
TELEGRAM_CHAT_ID = "8585819972"
STATE_FILE = "state.json"

PROMO_FOOTER = (
    "\n\n?? PASS YOUR PROP EVALUATION - NO MERCY."
    "\n? Grab the High-Volatility ATM Risk Setups & Playbooks NOW:"
    "\n?? https://thefundedbible.com"
    "\n?? USE CODE BIBLE80 AT CHECKOUT FOR 80% OFF - SECURE THE BAG."
)

try:
    with open(STATE_FILE, "r") as f:
        seen = json.load(f)
except:
    seen = {}

# Clean memory older than 2 hours so it doesn't bloat
now = time.time()
seen = {k: v for k, v in seen.items() if now - v < 7200}

def send_alert(msg):
    if not TELEGRAM_CHAT_ID: return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print("Telegram Error:", e)

FUTURES = {"NQ=F": "Nasdaq 100 (NQ)", "ES=F": "S&P 500 (ES)", "GC=F": "Gold (GC)", "BTC-USD": "Bitcoin (BTC)"}

for ticker, name in FUTURES.items():
    try:
        df = yf.Ticker(ticker).history(period="1d", interval="5m")
        if len(df) >= 4:
            c, p = float(df["Close"].iloc[-1]), float(df["Close"].iloc[-4])
            pct = ((c - p) / p) * 100
            key = f"{ticker}_{int(now // 1800)}"
            if abs(pct) >= 0.01 and key not in seen:
                seen[key] = now
                if pct > 0:
                    tag = "?? BULLISH BREAKOUT - INSTANT BUY PRESSURE"
                    direction_emoji = "??"
                else:
                    tag = "?? BEARISH LIQUIDITY FLUSH - MASSIVE SELL PRESSURE"
                    direction_emoji = "??"
                
                msg = (
                    f"?? HIGH-ALERT {direction_emoji} {tag}\n"
                    f"?? Asset: {name}\n"
                    f"?? Trade Price: {c:,.2f} ({pct:+.2f}% in 15m)\n"
                    f"?? Session Extreme: {float(df['Low'].min()):,.2f} - {float(df['High'].max()):,.2f}\n"
                    f"?? Tactical Play: Trailing drawdown is a target. Adjust risk now."
                    f"{PROMO_FOOTER}"
                )
                send_alert(msg)
    except Exception as e:
        pass

try:
    req = urllib.request.Request("https://api.dexscreener.com/latest/dex/search?q=WETH%20base", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        pairs = json.loads(resp.read().decode("utf-8")).get("pairs", [])
    for p in pairs[:5]:
        addr = p.get("pairAddress")
        vol = float(p.get("volume", {}).get("h1", 0) or 0)
        liq = float(p.get("liquidity", {}).get("usd", 0) or 0)
        chg = float(p.get("priceChange", {}).get("h1", 0) or 0)
        if addr and addr not in seen and vol >= 15000 and liq >= 10000 and chg >= 10:
            seen[addr] = now
            sym = p.get("baseToken", {}).get("symbol", "TOKEN")
            price = p.get("priceUsd", "0")
            msg = (
                f"?? BASE ON-CHAIN SURGE DETECTED ??\n"
                f"?? Asset: ${sym} Surge (+{chg:.1f}% 1H)\n"
                f"?? Unit Price: ${price}\n"
                f"?? 1H Velocity Volume: ${vol:,.0f} | ?? Pool Liquidity: ${liq:,.0f}\n"
                f"?? Tactical Note: Volatile micro-cap. Set profit triggers."
                f"{PROMO_FOOTER}"
            )
            send_alert(msg)
except: pass

# Save state for the next GitHub run
with open(STATE_FILE, "w") as f:
    json.dump(seen, f)
