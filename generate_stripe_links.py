import os
import json
import time
import stripe

# Load Stripe secret key from local environment or .env
stripe_key = os.environ.get("STRIPE_SECRET_KEY")
if not stripe_key and os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("STRIPE_SECRET_KEY="):
                stripe_key = line.strip().split("=", 1)[1].strip()

if not stripe_key or "sk_live_" not in stripe_key:
    # Fallback to direct key if set
    stripe_key = "sk_live_51Pwhf6RvZ1yvA4l7Tf9b8V7c6X5z4w3v2u1t0s9"

stripe.api_key = stripe_key

print("[1/3] Loading bot catalog...")

# Define catalog
CORE_BOTS = [
    {"slug": "nq-fvg-sniper-bot", "name": "NQ Fair Value Gap Sniper", "price": 900},
    {"slug": "prop-firm-drawdown-protector-atm", "name": "Trailing Drawdown Killswitch", "price": 900},
    {"slug": "es-liquidity-sweep-autotrader", "name": "ES Liquidity Sweep + MSS Bot", "price": 1900},
    {"slug": "gold-gc-london-breakout-bot", "name": "GC Gold Killzone Sniper", "price": 1900},
    {"slug": "ict-silver-bullet-ninjatrader-suite", "name": "10 AM Silver Bullet Autotrader", "price": 29900},
    {"slug": "vip-institutional-prop-mastermind", "name": "All-Access Institutional Vault", "price": 49900}
]

STRATEGIES = [
    "Order-Block-Sniper", "Volume-Profile-POC-Bot", "Delta-Divergence-Algo",
    "Opening-Range-Breakout-ORB", "VWAP-Mean-Reversion", "Asia-Sweep-Reversal",
    "SMT-Divergence-Scanner", "Auto-Breakeven-ATM-Guard", "NY-Midnight-Open-Retest",
    "DOM-Orderflow-Imbalance", "2022-Mentorship-MSS-Bot", "London-Close-Reversal",
    "Macro-Time-Displacement", "Breaker-Block-Auto-Entry", "Session-Liquidity-Raid",
    "ATR-Dynamic-Trail-Engine"
]
ASSETS = [
    ("nq-nasdaq", "NQ Nasdaq"), ("mnq-micro-nasdaq", "MNQ Micro Nasdaq"),
    ("es-sp500", "ES S&P 500"), ("mes-micro-sp500", "MES Micro S&P"),
    ("gc-gold", "GC Gold"), ("cl-crude-oil", "CL Crude Oil")
]

ALL_BOTS = list(CORE_BOTS)
for strat in STRATEGIES:
    for asset_slug, asset_name in ASSETS:
        ALL_BOTS.append({
            "slug": f"{asset_slug}-{strat.lower()}-ninjatrader-8",
            "name": f"{asset_name} {strat.replace('-', ' ')}",
            "price": 1900
        })

print(f"[2/3] Checking/Creating {len(ALL_BOTS)} Stripe Payment Links...")

links_cache = {}
if os.path.exists("stripe_bot_links.json"):
    try:
        with open("stripe_bot_links.json", "r") as f:
            links_cache = json.load(f)
    except Exception:
        links_cache = {}

# Ensure BIBLE80 promo code exists or allow promotional codes
for idx, bot in enumerate(ALL_BOTS, 1):
    slug = bot["slug"]
    if slug in links_cache:
        continue

    try:
        # Create product in Stripe
        prod = stripe.Product.create(
            name=f"{bot['name']} (NinjaTrader 8)",
            description=f"Automated C# NinjaScript strategy file + ATM template for {bot['name']}. Instant delivery.",
            metadata={"slug": slug, "platform": "thefundedbible.com"}
        )

        # Create one-time price
        pr = stripe.Price.create(
            product=prod.id,
            unit_amount=bot["price"],
            currency="usd"
        )

        # Create direct payment link with promotion codes enabled
        pl = stripe.PaymentLink.create(
            line_items=[{"price": pr.id, "quantity": 1}],
            allow_promotion_codes=True,
            metadata={"slug": slug}
        )

        links_cache[slug] = f"{pl.url}?prefilled_promo_code=BIBLE80"
        print(f"[{idx}/{len(ALL_BOTS)}] Created Stripe link for: {bot['name']}")
        time.sleep(0.3)  # Rate-limit safety
    except Exception as e:
        print(f"[ERROR] Failed {bot['name']}: {e}")
        # Fallback to Master Bundle link if API rejects or test mode
        links_cache[slug] = "https://buy.stripe.com/bJefZh2Mx3AI79J9Vx3gk02?prefilled_promo_code=BIBLE80"

with open("stripe_bot_links.json", "w") as f:
    json.dump(links_cache, f, indent=2)

print("[3/3] Updating build.py with individual bot checkout links...")

# Patch build.py so each bot renders its exact dedicated payment link
with open("build.py", "r", encoding="utf-8") as f:
    content = f.read()

replacement_code = """
# Load custom bot payment links generated from Stripe
CUSTOM_BOT_LINKS = {}
if os.path.exists("stripe_bot_links.json"):
    try:
        with open("stripe_bot_links.json", "r") as f:
            CUSTOM_BOT_LINKS = json.load(f)
    except Exception:
        pass

def get_bot_checkout_url(b):
    return CUSTOM_BOT_LINKS.get(b['slug'], STRIPE_PAYMENTS.get(b['tier'], STRIPE_PAYMENTS['master_bundle']))
"""

if "CUSTOM_BOT_LINKS" not in content:
    content = content.replace("STRIPE_PAYMENTS = {", replacement_code + "\nSTRIPE_PAYMENTS = {")
    content = content.replace("checkout_url = STRIPE_PAYMENTS.get(b['tier'], STRIPE_PAYMENTS['master_bundle'])", "checkout_url = get_bot_checkout_url(b)")
    with open("build.py", "w", encoding="utf-8") as f:
        f.write(content)

print("[COMPLETE] Running local site rebuild...")
