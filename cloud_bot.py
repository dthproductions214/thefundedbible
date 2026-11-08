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

SYMBOLS = {
    "NQ=F": {"name": "NQ (Nasdaq 100 Futures)", "tp_pts": 35.0, "sl_pts": 15.0},
    "ES=F": {"name": "ES (S&P 500 Futures)", "tp_pts": 12.0, "sl_pts": 5.0},
    "GC=F": {"name": "GC (Gold Futures)", "tp_pts": 8.0, "sl_pts": 3.5},
    "CL=F": {"name": "CL (Crude Oil Futures)", "tp_pts": 0.65, "sl_pts": 0.25}
}

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

def scan_market_and_signal():
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Scanning CME Futures for institutional setups...")
    
    for ticker, info in SYMBOLS.items():
        try:
            # period="5d" ensures data is retrieved even on weekends or pre-market
            df = yf.download(ticker, period="5d", interval="15m", progress=False)
            
            # If 15m is empty (e.g. weekend session transition), pull daily/hourly candles
            if df.empty or len(df) < 5:
                df = yf.download(ticker, period="5d", interval="1h", progress=False)

            if df.empty or len(df) < 3:
                print(f"[WARN] No data available right now for {ticker}")
                continue
            
            # Flatten multi-index columns if returned by newer yfinance
            if hasattr(df.columns, 'levels') and len(df.columns.levels) > 1:
                df.columns = df.columns.get_level_values(0)

            c1 = df.iloc[-3]
            c2 = df.iloc[-2]
            c3 = df.iloc[-1]

            current_price = float(c3['Close'])

            # Bullish Fair Value Gap / Expansion
            if float(c3['Low']) > float(c1['High']) and float(c2['Close']) > float(c2['Open']):
                signal_type = "BULLISH FVG EXPANSION (LONG)"
                entry = round(current_price, 2)
                sl = round(entry - info['sl_pts'], 2)
                tp = round(entry + info['tp_pts'], 2)
                bias_color = "🟢"
            # Bearish Fair Value Gap / Breakdown
            elif float(c3['High']) < float(c1['Low']) and float(c2['Close']) < float(c2['Open']):
                signal_type = "BEARISH FVG BREAKDOWN (SHORT)"
                entry = round(current_price, 2)
                sl = round(entry + info['sl_pts'], 2)
                tp = round(entry - info['tp_pts'], 2)
                bias_color = "🔴"
            else:
                ema_fast = df['Close'].rolling(window=5).mean().iloc[-1]
                ema_slow = df['Close'].rolling(window=13).mean().iloc[-1]
                if ema_fast >= ema_slow:
                    signal_type = "ORDERFLOW MOMENTUM LONG"
                    entry = round(current_price, 2)
                    sl = round(entry - info['sl_pts'], 2)
                    tp = round(entry + info['tp_pts'], 2)
                    bias_color = "🟢"
                else:
                    signal_type = "LIQUIDITY RUN SHORT"
                    entry = round(current_price, 2)
                    sl = round(entry + info['sl_pts'], 2)
                    tp = round(entry - info['tp_pts'], 2)
                    bias_color = "🔴"

            message = (
                f"{bias_color} <b>LIVE INSTITUTIONAL SIGNAL | THE FUNDED BIBLE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📊 <b>Asset:</b> {info['name']}\n"
                f"⚡ <b>Setup:</b> {signal_type}\n"
                f"🎯 <b>Entry Zone:</b> <code>{entry}</code>\n"
                f"🛑 <b>Hard Stop (SL):</b> <code>{sl}</code>\n"
                f"💰 <b>Take Profit (TP):</b> <code>{tp}</code>\n"
                f"🛡️ <b>Risk:</b> 1-2 Contracts Max (Prop Rule Lock)\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🔥 <i>Automate this setup with our $9 NinjaScript Bot:</i>\n"
                f"👉 <a href='{SITE_URL}'>thefundedbible.com</a>\n"
                f"🏷️ <i>Prop Firm Code:</i> <b>BIBLE80</b> (Max Discount)"
            )

            send_telegram_alert(message)
            print(f"[SUCCESS] Dispatched live signal for {ticker} -> Telegram")
            time.sleep(2)

        except Exception as e:
            print(f"[ERROR] Symbol {ticker} scan: {e}")

if __name__ == "__main__":
    scan_market_and_signal()
