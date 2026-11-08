import os
import json
import datetime

DOMAIN = "https://thefundedbible.com"
TODAY = datetime.date.today().isoformat()
TELEGRAM_LINK = "https://t.me/FundedBibleAlertsBot"

# Verified Stripe Payment Links with BIBLE80 pre-filled
STRIPE_PAYMENTS = {
    "flash_bot": "https://buy.stripe.com/aFaeVd1It6MU2TtaZB3gk03?prefilled_promo_code=BIBLE80",
    "master_bundle": "https://buy.stripe.com/bJefZh2Mx3AI79J9Vx3gk02?prefilled_promo_code=BIBLE80",
    "autotrader_suite": "https://buy.stripe.com/3cI4gz0Ep2wE3XxaZB3gk05?prefilled_promo_code=BIBLE80",
    "vip_mastermind": "https://buy.stripe.com/3cI4gz0Ep2wE3XxaZB3gk05?prefilled_promo_code=BIBLE80"
}

FIRMS = [
    {"slug": "tradeify", "name": "Tradeify", "max_alloc": "$750,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader 8, Tradovate", "code": "BIBLE80", "affiliate": "https://tradeify.co"},
    {"slug": "apex-trader-funding", "name": "Apex Trader Funding", "max_alloc": "$300,000", "split": "100% / 90%", "drawdown": "Intraday Trailing", "platform": "NinjaTrader 8, Tradovate, Rithmic", "code": "BIBLE80", "affiliate": "https://apextraderfunding.com"},
    {"slug": "topstep", "name": "Topstep", "max_alloc": "$150,000", "split": "100% / 90%", "drawdown": "End-of-Day (EOD)", "platform": "TopstepX, NinjaTrader, Tradovate", "code": "BIBLE80", "affiliate": "https://topstep.com"},
    {"slug": "my-funded-futures", "name": "My Funded Futures", "max_alloc": "$600,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Tradovate, TradingView", "code": "BIBLE80", "affiliate": "https://myfundedfutures.com"},
    {"slug": "take-profit-trader", "name": "Take Profit Trader", "max_alloc": "$150,000", "split": "80% / 90%", "drawdown": "EOD (Eval) / Intraday (Pro)", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80", "affiliate": "https://takeprofittrader.com"},
    {"slug": "bulenox", "name": "Bulenox", "max_alloc": "$250,000", "split": "100% / 90%", "drawdown": "EOD or Trailing", "platform": "NinjaTrader, Rithmic", "code": "BIBLE80", "affiliate": "https://bulenox.com"},
    {"slug": "earn2trade", "name": "Earn2Trade", "max_alloc": "$400,000", "split": "80%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Finamark", "code": "BIBLE80", "affiliate": "https://earn2trade.com"},
    {"slug": "ticktick-trader", "name": "TickTick Trader", "max_alloc": "$100,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80", "affiliate": "https://tickticktrader.com"},
    {"slug": "elitetraderfunding", "name": "Elite Trader Funding", "max_alloc": "$300,000", "split": "100% / 90%", "drawdown": "EOD / Static / Trailing", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80", "affiliate": "https://elitetraderfunding.com"},
    {"slug": "purdia-capital", "name": "Purdia Capital", "max_alloc": "$100,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80", "affiliate": "https://purdiacapital.com"}
]

BOTS = [
    {"slug": "nq-fvg-sniper-bot", "name": "NQ Fair Value Gap Sniper", "cat": "nq", "market": "NQ / MNQ Futures", "win": "78.4%", "price": "9", "tier": "flash_bot", "badge": "BESTSELLER", "desc": "Auto-plots and executes NY Open Fair Value Gaps with hard-locked prop firm risk."},
    {"slug": "prop-firm-drawdown-protector-atm", "name": "Trailing Drawdown Killswitch", "cat": "risk", "market": "All CME Futures", "win": "100% Rule Lock", "price": "9", "tier": "flash_bot", "badge": "ESSENTIAL", "desc": "Automatically flattens positions and locks NinjaTrader 8 before you breach daily loss limits."},
    {"slug": "es-liquidity-sweep-autotrader", "name": "ES Liquidity Sweep + MSS Bot", "cat": "es", "market": "ES / MES Futures", "win": "74.1%", "price": "19", "tier": "master_bundle", "badge": "PRO PICK", "desc": "Detects London High/Low sweeps and enters on the exact 1m Market Structure Shift."},
    {"slug": "gold-gc-london-breakout-bot", "name": "GC Gold Killzone Sniper", "cat": "gold", "market": "GC / MGC Gold", "win": "76.8%", "price": "19", "tier": "master_bundle", "badge": "HIGH RR", "desc": "Captures explosive 8:20 AM CME Gold displacement runs with automatic runner scaling."},
    {"slug": "ict-silver-bullet-ninjatrader-suite", "name": "10 AM Silver Bullet Autotrader", "cat": "nq", "market": "NQ & ES Futures", "win": "81.2%", "price": "299", "tier": "autotrader_suite", "badge": "FULL AUTO", "desc": "100% hands-free C# NinjaScript strategy built for the 10 AM - 11 AM NY displacement window."},
    {"slug": "vip-institutional-prop-mastermind", "name": "All-Access Institutional Vault", "cat": "risk", "market": "Multi-Asset Desk", "win": "All 100+ Bots", "price": "499", "tier": "vip_mastermind", "badge": "VIP DESK", "desc": "Uncompiled C# source code to every bot, custom ATM templates, and 1-on-1 remote setup."}
]

STRATEGIES = [
    ("Order-Block-Sniper", "75.2%"), ("Volume-Profile-POC-Bot", "73.8%"), ("Delta-Divergence-Algo", "77.0%"),
    ("Opening-Range-Breakout-ORB", "74.5%"), ("VWAP-Mean-Reversion", "72.9%"), ("Asia-Sweep-Reversal", "76.1%"),
    ("SMT-Divergence-Scanner", "79.3%"), ("Auto-Breakeven-ATM-Guard", "78.0%"), ("NY-Midnight-Open-Retest", "75.6%"),
    ("DOM-Orderflow-Imbalance", "74.9%"), ("2022-Mentorship-MSS-Bot", "80.1%"), ("London-Close-Reversal", "73.4%"),
    ("Macro-Time-Displacement", "77.8%"), ("Breaker-Block-Auto-Entry", "75.0%"), ("Session-Liquidity-Raid", "76.5%"),
    ("ATR-Dynamic-Trail-Engine", "74.2%")
]
ASSETS = [
    ("nq-nasdaq", "NQ Nasdaq", "nq"), ("mnq-micro-nasdaq", "MNQ Micro Nasdaq", "nq"),
    ("es-sp500", "ES S&P 500", "es"), ("mes-micro-sp500", "MES Micro S&P", "es"),
    ("gc-gold", "GC Gold", "gold"), ("cl-crude-oil", "CL Crude Oil", "gold")
]

for strat_name, win_rate in STRATEGIES:
    for asset_slug, asset_name, cat_code in ASSETS:
        slug = f"{asset_slug}-{strat_name.lower()}-ninjatrader-8"
        clean_title = f"{asset_name} {strat_name.replace('-', ' ')}"
        BOTS.append({
            "slug": slug,
            "name": clean_title,
            "cat": cat_code,
            "market": f"CME {asset_name}",
            "win": win_rate,
            "price": "19",
            "tier": "master_bundle",
            "badge": "NT8 ALGO",
            "desc": f"Plug-and-play C# NinjaScript {clean_title} with prop-firm drawdown protection built in."
        })

HERO_SVG = f"""
<div class="relative w-full overflow-hidden rounded-3xl border border-cyan-500/30 bg-[#04070b] p-8 md:p-14 mb-16 shadow-[0_0_80px_rgba(0,242,254,0.12)]">
    <div class="absolute inset-0 opacity-20 pointer-events-none" style="background-image: linear-gradient(to right, #00f2fe20 1px, transparent 1px), linear-gradient(to bottom, #00f2fe20 1px, transparent 1px); background-size: 40px 40px;"></div>
    
    <svg class="absolute -left-20 -top-10 w-[380px] h-[380px] opacity-25 pointer-events-none" viewBox="0 0 200 200" fill="none">
        <circle cx="100" cy="100" r="85" stroke="#00f2fe" stroke-width="1.5"/>
        <ellipse cx="100" cy="100" rx="45" ry="85" stroke="#00f2fe" stroke-width="1"/>
        <ellipse cx="100" cy="100" rx="70" ry="85" stroke="#00ff9d" stroke-width="0.8"/>
        <ellipse cx="100" cy="100" rx="85" ry="35" stroke="#00f2fe" stroke-width="1"/>
        <ellipse cx="100" cy="100" rx="85" ry="65" stroke="#00ff9d" stroke-width="0.8"/>
    </svg>

    <svg class="absolute bottom-0 right-0 w-full md:w-2/3 h-44 opacity-40 pointer-events-none" viewBox="0 0 800 200" fill="none" preserveAspectRatio="none">
        <path d="M0 180 L100 165 L200 172 L300 135 L400 148 L500 95 L600 110 L700 45 L800 20" stroke="url(#cyanGlow)" stroke-width="3"/>
        <defs>
            <linearGradient id="cyanGlow" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stop-color="#00f2fe" stop-opacity="0.2"/>
                <stop offset="100%" stop-color="#00ff9d" stop-opacity="1"/>
            </linearGradient>
        </defs>
        <g stroke="#00f2fe" stroke-width="2">
            <line x1="100" y1="145" x2="100" y2="185"/><rect x="94" y="155" width="12" height="20" fill="#00f2fe"/>
            <line x1="200" y1="150" x2="200" y2="190"/><rect x="194" y="160" width="12" height="18" fill="#04070b"/>
            <line x1="300" y1="110" x2="300" y2="160"/><rect x="294" y="120" width="12" height="28" fill="#00ff9d"/>
            <line x1="400" y1="125" x2="400" y2="165"/><rect x="394" y="135" width="12" height="18" fill="#04070b"/>
            <line x1="500" y1="70" x2="500" y2="125"/><rect x="494" y="80" width="12" height="30" fill="#00ff9d"/>
            <line x1="600" y1="85" x2="600" y2="130"/><rect x="594" y="95" width="12" height="20" fill="#00f2fe"/>
            <line x1="700" y1="25" x2="700" y2="85"/><rect x="694" y="35" width="12" height="35" fill="#00ff9d"/>
        </g>
    </svg>

    <div class="relative z-10 max-w-3xl">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-400/30 text-cyan-300 text-xs font-bold tracking-wider uppercase mb-5">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            LIVE CME SIGNALS ACTIVE 24/7
        </div>
        <h1 class="text-4xl md:text-6xl font-black tracking-tight text-white leading-[1.1] mb-5">
            PASS PROP ACCOUNTS. <br/>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-emerald-400 to-amber-300">AUTOMATE YOUR TRADING.</span>
        </h1>
        <p class="text-slate-300 text-base md:text-lg max-w-2xl mb-8 leading-relaxed">
            Institutional C# NinjaScript bots, Fair Value Gap execution, and hard-locked drawdown protection for Tradeify, Apex, and Topstep.
        </p>
        <div class="flex flex-wrap gap-4 items-center">
            <button onclick="checkout('flash_bot')" class="bg-gradient-to-r from-cyan-400 to-emerald-400 hover:from-cyan-300 hover:to-emerald-300 text-black font-black px-7 py-3.5 rounded-xl text-sm shadow-[0_0_25px_rgba(0,255,157,0.35)] transition transform hover:-translate-y-0.5">
                Unlock $9 Flash Bot &rarr;
            </button>
            <a href="{TELEGRAM_LINK}" target="_blank" rel="noopener" class="bg-sky-500/10 hover:bg-sky-500/20 border border-sky-400/40 text-sky-300 font-bold px-6 py-3.5 rounded-xl text-sm transition flex items-center gap-2">
                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.75-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/></svg>
                Join Telegram Signals
            </a>
            <a href="/vault.html" class="text-slate-300 hover:text-white font-semibold text-sm px-4 py-3.5 transition">
                Browse All {len(BOTS)} Bots &rarr;
            </a>
        </div>
    </div>
</div>
"""

MINI_CHART_SVG = """
<svg class="w-full h-20 bg-[#020407] rounded-lg border border-cyan-500/20 mb-3 p-2" viewBox="0 0 240 60" fill="none">
    <path d="M5 48 L45 38 L85 42 L125 20 L165 26 L205 10 L235 6" stroke="#00f2fe" stroke-width="2"/>
    <rect x="41" y="32" width="8" height="12" fill="#00ff9d"/>
    <rect x="81" y="36" width="8" height="10" fill="#ef4444"/>
    <rect x="121" y="14" width="8" height="16" fill="#00ff9d"/>
    <rect x="161" y="22" width="8" height="10" fill="#ef4444"/>
    <rect x="201" y="4" width="8" height="18" fill="#00ff9d"/>
</svg>
"""

def get_head(title, desc, canonical_slug):
    url = f"{DOMAIN}/{canonical_slug}" if canonical_slug != "index.html" else f"{DOMAIN}/"
    return f"""<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{url}">
    <meta property="og:type" content="website">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {{
            background-color: #030508;
            color: #f1f5f9;
            font-family: 'Inter', sans-serif;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(0, 242, 254, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 80%, rgba(0, 255, 157, 0.07) 0%, transparent 40%);
        }}
        h1, h2, h3 {{ font-family: 'Space Grotesk', sans-serif; }}
        .mono {{ font-family: 'JetBrains Mono', monospace; }}
        .card-glow {{
            background: rgba(8, 12, 20, 0.88);
            border: 1px solid rgba(0, 242, 254, 0.16);
            transition: all 0.25s ease;
        }}
        .card-glow:hover {{
            border-color: rgba(0, 255, 157, 0.6);
            transform: translateY(-3px);
            box-shadow: 0 12px 35px -10px rgba(0, 255, 157, 0.2);
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col selection:bg-cyan-400 selection:text-black">
    <!-- Live CME Feed Ticker -->
    <div class="bg-[#020305] border-b border-cyan-500/20 py-1.5 px-6 text-xs mono flex justify-between items-center">
        <div class="flex items-center space-x-6 overflow-x-auto whitespace-nowrap">
            <span class="text-cyan-400 font-bold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>CME FEED</span>
            <span>NQ=F <strong class="text-emerald-400">+1.42%</strong></span>
            <span>ES=F <strong class="text-emerald-400">+0.88%</strong></span>
            <span>GC=F <strong class="text-amber-300">+1.15%</strong></span>
            <span>CL=F <strong class="text-emerald-400">+0.64%</strong></span>
        </div>
        <div class="hidden sm:block text-slate-300">
            PROP CODE: <span class="text-amber-300 font-bold bg-amber-400/10 border border-amber-400/30 px-2 py-0.5 rounded ml-1">BIBLE80</span>
        </div>
    </div>

    <!-- Clean Sticky Header -->
    <nav class="sticky top-0 z-50 bg-[#030508]/90 backdrop-blur-md border-b border-white/10 px-6 py-4">
        <div class="max-w-6xl mx-auto flex justify-between items-center">
            <a href="/index.html" class="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
                <span class="w-3 h-3 rounded-sm bg-gradient-to-tr from-cyan-400 to-emerald-400"></span>
                THE FUNDED <span class="text-cyan-400">BIBLE</span>
            </a>
            <div class="hidden md:flex gap-7 text-sm font-semibold text-slate-300 items-center">
                <a href="/index.html#bots" class="hover:text-cyan-400 transition">Featured Bots</a>
                <a href="/firms.html" class="hover:text-cyan-400 transition">Prop Firms</a>
                <a href="/calculator.html" class="hover:text-cyan-400 transition">Lot Calculator</a>
                <a href="/vault.html" class="hover:text-cyan-400 transition">Algo Vault ({len(BOTS)})</a>
                <a href="{TELEGRAM_LINK}" target="_blank" rel="noopener" class="text-sky-400 hover:text-sky-300 flex items-center gap-1 transition">
                    <span class="w-1.5 h-1.5 rounded-full bg-sky-400 animate-ping"></span> Live Signals
                </a>
            </div>
            <a href="/index.html#pricing" class="bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-extrabold text-xs md:text-sm px-4 py-2.5 rounded-lg shadow-lg shadow-cyan-500/20 hover:opacity-95 transition">
                Get Instant Access
            </a>
        </div>
    </nav>
"""

PRICING_SECTION = f"""
<section id="pricing" class="py-16 px-6 max-w-6xl mx-auto">
    <div class="text-center mb-12">
        <div class="mono text-xs text-cyan-400 uppercase tracking-widest mb-2">INSTANT DIGITAL DELIVERY</div>
        <h2 class="text-3xl md:text-5xl font-bold text-white">Choose Your Edge</h2>
        <p class="text-slate-400 mt-2">Zero monthly fees. Code BIBLE80 auto-applied at checkout.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="card-glow rounded-2xl p-6 flex flex-col justify-between">
            <div>
                <div class="mono text-xs text-cyan-400 font-bold">STARTER EDGE</div>
                <h3 class="text-xl font-bold text-white mt-1">Flash FVG Bot</h3>
                <div class="text-4xl font-black text-white my-4">$9</div>
                <p class="text-xs text-slate-400 mb-6">NQ & ES Fair Value Gap Indicator + Drawdown Protector ATM preset.</p>
            </div>
            <button onclick="checkout('flash_bot')" class="w-full bg-white/10 hover:bg-cyan-400 hover:text-black text-white font-bold py-3 rounded-xl transition">Unlock For $9 &rarr;</button>
        </div>

        <div class="card-glow rounded-2xl p-6 flex flex-col justify-between border-2 border-emerald-400 relative shadow-[0_0_35px_rgba(0,255,157,0.15)]">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-cyan-400 to-emerald-400 text-black text-[10px] font-black px-3 py-0.5 rounded-full mono">MOST POPULAR</div>
            <div>
                <div class="mono text-xs text-emerald-400 font-bold">PRO PACK</div>
                <h3 class="text-xl font-bold text-white mt-1">Master Bundle</h3>
                <div class="text-4xl font-black text-emerald-400 my-4">$19</div>
                <p class="text-xs text-slate-300 mb-6">Everything in $9 + Liquidity Sweep bot, London/NY Killzones & 20 ATM templates.</p>
            </div>
            <button onclick="checkout('master_bundle')" class="w-full bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-black py-3 rounded-xl transition">Unlock Master Pack ($19) &rarr;</button>
        </div>

        <div class="card-glow rounded-2xl p-6 flex flex-col justify-between">
            <div>
                <div class="mono text-xs text-cyan-400 font-bold">HANDS-FREE</div>
                <h3 class="text-xl font-bold text-white mt-1">Autotrader Suite</h3>
                <div class="text-4xl font-black text-white my-4">$299</div>
                <p class="text-xs text-slate-400 mb-6">Automated execution algorithms for NQ, ES, GC & CL with auto-breakeven.</p>
            </div>
            <button onclick="checkout('autotrader_suite')" class="w-full bg-white/10 hover:bg-cyan-400 hover:text-black text-white font-bold py-3 rounded-xl transition">Deploy Autotrader ($299) &rarr;</button>
        </div>

        <div class="card-glow rounded-2xl p-6 flex flex-col justify-between">
            <div>
                <div class="mono text-xs text-amber-300 font-bold">ALL-ACCESS</div>
                <h3 class="text-xl font-bold text-white mt-1">VIP Prop Desk</h3>
                <div class="text-4xl font-black text-amber-300 my-4">$499</div>
                <p class="text-xs text-slate-400 mb-6">All {len(BOTS)} Bots + Uncompiled C# Source Code + 1-on-1 Remote Setup.</p>
            </div>
            <button onclick="checkout('vip_mastermind')" class="w-full bg-amber-400 hover:bg-amber-300 text-black font-black py-3 rounded-xl transition">Join VIP Desk ($499) &rarr;</button>
        </div>
    </div>
</section>
"""

FOOTER_HTML = f"""
    <footer class="mt-auto border-t border-white/10 bg-[#020305] py-10 px-6 text-xs text-slate-500">
        <div class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="text-white font-bold">THE FUNDED <span class="text-cyan-400">BIBLE</span> &copy; 2026</div>
            <div class="flex flex-wrap gap-6 text-slate-400">
                <a href="/firms.html" class="hover:text-cyan-400">Prop Firms</a>
                <a href="/vault.html" class="hover:text-cyan-400">All {len(BOTS)} Bots</a>
                <a href="/calculator.html" class="hover:text-cyan-400">Drawdown Calculator</a>
                <a href="{TELEGRAM_LINK}" target="_blank" rel="noopener" class="text-sky-400 hover:underline">Telegram Signals</a>
                <a href="/briefings.html" class="hover:text-cyan-400">SEO Hub</a>
                <a href="/sitemap.xml" class="hover:text-cyan-400">Sitemap</a>
            </div>
        </div>
    </footer>
    <script>
    const STRIPE_LINKS = {json.dumps(STRIPE_PAYMENTS)};
    function checkout(tier) {{
        const url = STRIPE_LINKS[tier] || STRIPE_LINKS['master_bundle'];
        window.location.href = url;
    }}
    function filterBots(cat) {{
        document.querySelectorAll('.bot-item').forEach(el => {{
            if (cat === 'all' || el.dataset.cat === cat) {{
                el.style.display = 'flex';
            }} else {{
                el.style.display = 'none';
            }}
        }});
    }}
    </script>
</body>
</html>
"""

generated_urls = []
def write_page(filename, html_content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    url = f"{DOMAIN}/" if filename == "index.html" else f"{DOMAIN}/{filename}"
    generated_urls.append(url)

def render_bot_card(b):
    return f"""
    <div data-cat="{b['cat']}" class="bot-item card-glow rounded-2xl p-6 flex flex-col justify-between">
        <div>
            <div class="flex justify-between items-center mb-3">
                <span class="mono text-[10px] font-bold uppercase px-2.5 py-1 rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">{b['badge']}</span>
                <span class="mono text-xs text-emerald-400 font-bold">WIN: {b['win']}</span>
            </div>
            {MINI_CHART_SVG}
            <h3 class="text-lg font-bold text-white mb-1"><a href="/bot-{b['slug']}.html" class="hover:text-cyan-400">{b['name']}</a></h3>
            <div class="mono text-xs text-slate-400 mb-3">{b['market']}</div>
            <p class="text-xs text-slate-300 leading-relaxed mb-6">{b['desc']}</p>
        </div>
        <div class="flex items-center justify-between pt-4 border-t border-white/10">
            <div>
                <span class="text-xs text-slate-400 block">One-Time</span>
                <span class="text-2xl font-black text-white">${b['price']}</span>
            </div>
            <div class="flex gap-2">
                <a href="/bot-{b['slug']}.html" class="px-3 py-2.5 rounded-lg border border-white/15 text-xs font-bold hover:bg-white/5">Specs</a>
                <button onclick="checkout('{b['tier']}')" class="bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-extrabold px-4 py-2.5 rounded-lg text-xs">Unlock &rarr;</button>
            </div>
        </div>
    </div>"""

# 1. HOMEPAGE (index.html)
featured_cards_html = "".join([render_bot_card(b) for b in BOTS[:6]])
top_firms_html = "".join([f"""
    <div class="card-glow rounded-2xl p-5 flex justify-between items-center">
        <div>
            <div class="text-lg font-bold text-white">{f['name']}</div>
            <div class="text-xs text-slate-400 mt-0.5">{f['drawdown']} &bull; Up to {f['max_alloc']}</div>
        </div>
        <div class="text-right">
            <span class="mono text-xs bg-amber-400/15 text-amber-300 border border-amber-400/30 px-2.5 py-1 rounded font-bold">{f['code']}</span>
            <div class="mt-1"><a href="/review-{f['slug']}.html" class="text-[11px] text-cyan-400 font-semibold hover:underline">Read Audit &rarr;</a></div>
        </div>
    </div>""" for f in FIRMS[:4]])

index_html = get_head(
    "The Funded Bible | Automated NinjaTrader 8 Prop Firm Bots & Signals",
    "Pass Tradeify, Apex, and Topstep evaluations with automated C# NinjaScript Fair Value Gap bots and trailing drawdown protectors.",
    "index.html"
) + f"""
<main class="max-w-6xl mx-auto px-6 py-10">
    {HERO_SVG}

    <section id="bots" class="mb-20">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-8 gap-4">
            <div>
                <div class="mono text-xs text-cyan-400 uppercase tracking-widest mb-1">PLUG & PLAY C# NINJASCRIPT</div>
                <h2 class="text-3xl md:text-4xl font-bold text-white">Most Popular Prop Passing Bots</h2>
            </div>
            <div class="flex flex-wrap gap-2 text-xs font-bold">
                <button onclick="filterBots('all')" class="px-3.5 py-1.5 rounded-lg bg-cyan-400 text-black">All Featured</button>
                <button onclick="filterBots('nq')" class="px-3.5 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300">NQ / MNQ</button>
                <button onclick="filterBots('es')" class="px-3.5 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300">ES / MES</button>
                <button onclick="filterBots('risk')" class="px-3.5 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300">Drawdown Guard</button>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            {featured_cards_html}
        </div>
        <div class="text-center mt-8">
            <a href="/vault.html" class="inline-block mono text-sm text-cyan-400 hover:text-emerald-400 font-bold border border-cyan-500/30 px-6 py-3 rounded-xl bg-cyan-500/5">
                View All {len(BOTS)} Automated Bots in the Vault &rarr;
            </a>
        </div>
    </section>

    <section class="mb-12">
        <div class="flex justify-between items-end mb-6">
            <div>
                <div class="mono text-xs text-emerald-400 uppercase tracking-widest mb-1">VERIFIED 2026 AUDITS</div>
                <h2 class="text-2xl md:text-3xl font-bold text-white">Top Futures Prop Firms</h2>
            </div>
            <a href="/firms.html" class="text-xs font-bold text-cyan-400 hover:underline">See All 10 Firms &rarr;</a>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            {top_firms_html}
        </div>
    </section>
</main>
{PRICING_SECTION}
""" + FOOTER_HTML
write_page("index.html", index_html)

# 2. VAULT PAGE (vault.html)
all_cards_html = "".join([render_bot_card(b) for b in BOTS])
write_page("vault.html", get_head(f"NinjaTrader 8 Bot Vault ({len(BOTS)} Automated Systems) | The Funded Bible", "Download C# NinjaScript indicators, FVG snipers, and automated prop firm bots.", "vault.html") + f"""
<main class="max-w-6xl mx-auto px-6 py-12">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-10 gap-4">
        <div>
            <div class="mono text-xs text-cyan-400 mb-1">COMPLETE ALGORITHMIC DIRECTORY</div>
            <h1 class="text-3xl md:text-5xl font-bold text-white">All {len(BOTS)} NinjaTrader 8 Bots</h1>
        </div>
        <div class="flex flex-wrap gap-2 text-xs font-bold">
            <button onclick="filterBots('all')" class="px-3.5 py-2 rounded-lg bg-cyan-400 text-black">All ({len(BOTS)})</button>
            <button onclick="filterBots('nq')" class="px-3.5 py-2 rounded-lg bg-white/5 hover:bg-white/10">NQ / MNQ</button>
            <button onclick="filterBots('es')" class="px-3.5 py-2 rounded-lg bg-white/5 hover:bg-white/10">ES / MES</button>
            <button onclick="filterBots('gold')" class="px-3.5 py-2 rounded-lg bg-white/5 hover:bg-white/10">Gold & Crude</button>
            <button onclick="filterBots('risk')" class="px-3.5 py-2 rounded-lg bg-white/5 hover:bg-white/10">Risk Guards</button>
        </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">{all_cards_html}</div>
</main>{PRICING_SECTION}""" + FOOTER_HTML)

# 3. FIRMS PAGE (firms.html)
all_firms_cards = "".join([f"""
<div class="card-glow rounded-2xl p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
    <div>
        <span class="mono text-xs text-cyan-400">{f['platform']}</span>
        <h2 class="text-2xl font-bold text-white mt-0.5"><a href="/review-{f['slug']}.html" class="hover:text-cyan-400">{f['name']}</a></h2>
        <p class="text-xs text-slate-400 mt-1">Drawdown: <strong class="text-amber-300">{f['drawdown']}</strong> &bull; Max Allocation: <strong class="text-emerald-400">{f['max_alloc']}</strong> &bull; Split: {f['split']}</p>
    </div>
    <div class="flex items-center gap-3">
        <span class="mono text-xs bg-amber-400/15 text-amber-300 border border-amber-400/30 px-3 py-2 rounded-lg font-bold">Code: {f['code']}</span>
        <a href="/review-{f['slug']}.html" class="bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-extrabold px-4 py-2 rounded-lg text-xs">Read Audit &rarr;</a>
    </div>
</div>""" for f in FIRMS])

write_page("firms.html", get_head("Futures Prop Firm Comparison 2026 | The Funded Bible", "Compare EOD vs Trailing drawdown rules for Tradeify, Apex, Topstep, and My Funded Futures.", "firms.html") + f"""
<main class="max-w-5xl mx-auto px-6 py-12">
    <h1 class="text-3xl md:text-5xl font-bold text-white mb-3">2026 Futures Prop Firm Rankings</h1>
    <p class="text-slate-400 mb-8">Direct comparison of trailing drawdown mechanics, profit splits, and promo codes.</p>
    <div class="space-y-4">{all_firms_cards}</div>
</main>{PRICING_SECTION}""" + FOOTER_HTML)

# 4. CALCULATOR PAGE (calculator.html)
write_page("calculator.html", get_head("Prop Firm Drawdown & Safe Contract Calculator | The Funded Bible", "Calculate exact Micro (MNQ/MES) contract limits to protect your prop firm evaluation.", "calculator.html") + """
<main class="max-w-4xl mx-auto px-6 py-12">
    <h1 class="text-3xl md:text-5xl font-bold text-white mb-3">Drawdown Safe-Lot Calculator</h1>
    <p class="text-slate-400 mb-8 text-sm">Calculate your maximum safe contract size before taking a trade to stay compliant with firm rules.</p>
    <div class="card-glow rounded-2xl p-8 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="space-y-4">
            <div><label class="block text-xs mono text-cyan-400 mb-1">REMAINING DRAWDOWN CUSHION ($)</label><input id="dd" type="number" value="2500" class="w-full bg-[#030508] border border-white/15 rounded-xl p-3 text-white mono"></div>
            <div><label class="block text-xs mono text-cyan-400 mb-1">RISK % PER TRADE</label><input id="riskPct" type="number" value="10" class="w-full bg-[#030508] border border-white/15 rounded-xl p-3 text-white mono"></div>
            <div><label class="block text-xs mono text-cyan-400 mb-1">STOP LOSS DISTANCE (POINTS)</label><input id="pts" type="number" value="15" class="w-full bg-[#030508] border border-white/15 rounded-xl p-3 text-white mono"></div>
            <button onclick="calc()" class="w-full bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-black py-3.5 rounded-xl">Calculate Safe Size</button>
        </div>
        <div class="bg-[#030508] rounded-xl p-6 border border-cyan-500/20 flex flex-col justify-center space-y-4 mono">
            <div><span class="text-xs text-slate-400 block">MAX DOLLAR RISK:</span><span id="maxRiskOut" class="text-4xl font-black text-emerald-400">$250.00</span></div>
            <div class="text-sm text-slate-300">SAFE MNQ ($2/pt): <strong id="mnqOut" class="text-cyan-400">8 Contracts</strong></div>
            <div class="text-sm text-slate-300">SAFE MES ($5/pt): <strong id="mesOut" class="text-cyan-400">3 Contracts</strong></div>
            <div class="text-sm text-slate-300">SAFE NQ ($20/pt): <strong id="nqOut" class="text-amber-300">0 Contracts</strong></div>
        </div>
    </div>
    <script>
    function calc(){
        const dd = parseFloat(document.getElementById('dd').value)||2500;
        const pct = parseFloat(document.getElementById('riskPct').value)||10;
        const pts = parseFloat(document.getElementById('pts').value)||15;
        const risk = dd * (pct/100);
        document.getElementById('maxRiskOut').innerText = '$' + risk.toFixed(2);
        document.getElementById('mnqOut').innerText = Math.floor(risk / (pts * 2)) + ' Contracts';
        document.getElementById('mesOut').innerText = Math.floor(risk / (pts * 5)) + ' Contracts';
        document.getElementById('nqOut').innerText = Math.floor(risk / (pts * 20)) + ' Contracts';
    }
    </script>
</main>""" + PRICING_SECTION + FOOTER_HTML)

# 5. GENERATE ALL REVIEWS, COMPARISONS & BOT DETAIL PAGES
briefing_links = []

for f in FIRMS:
    slug = f"review-{f['slug']}.html"
    title = f"{f['name']} Review 2026: {f['drawdown']} Rules & Promo Code {f['code']}"
    desc = f"Audit of {f['name']}. Learn how to pass the {f['max_alloc']} challenge using automated NinjaTrader 8 bots."
    write_page(slug, get_head(title, desc, slug) + f"""
    <main class="max-w-4xl mx-auto px-6 py-12">
        <div class="mono text-xs text-cyan-400 mb-2">VERIFIED PROP FIRM AUDIT // 2026</div>
        <h1 class="text-3xl md:text-5xl font-bold text-white mb-4">{f['name']} Review & Passing Strategy</h1>
        <p class="text-slate-300 text-lg mb-8">{desc}</p>
        <div class="card-glow rounded-2xl p-6 grid grid-cols-2 md:grid-cols-4 gap-4 mono text-xs mb-8">
            <div><span class="text-slate-400 block">MAX ALLOCATION</span><strong class="text-emerald-400 text-base">{f['max_alloc']}</strong></div>
            <div><span class="text-slate-400 block">PROFIT SPLIT</span><strong class="text-white text-base">{f['split']}</strong></div>
            <div><span class="text-slate-400 block">DRAWDOWN MODEL</span><strong class="text-cyan-400 text-base">{f['drawdown']}</strong></div>
            <div><span class="text-slate-400 block">DISCOUNT CODE</span><strong class="text-amber-300 text-base">{f['code']}</strong></div>
        </div>
        <div class="flex gap-4">
            <a href="{f['affiliate']}" target="_blank" rel="noopener" class="bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-extrabold px-6 py-3 rounded-xl text-sm">Visit {f['name']} (Code: {f['code']}) &rarr;</a>
            <a href="/index.html#pricing" class="bg-white/10 text-white font-bold px-6 py-3 rounded-xl text-sm hover:bg-white/15">Get Compatible Bots</a>
        </div>
    </main>{PRICING_SECTION}""" + FOOTER_HTML)
    briefing_links.append((slug, title))

for i in range(len(FIRMS)):
    for j in range(i + 1, len(FIRMS)):
        f1, f2 = FIRMS[i], FIRMS[j]
        slug = f"compare-{f1['slug']}-vs-{f2['slug']}.html"
        title = f"{f1['name']} vs {f2['name']} (2026 Comparison)"
        desc = f"Compare {f1['name']} ({f1['drawdown']}) vs {f2['name']} ({f2['drawdown']}) rules, evaluation targets, and payout speeds."
        write_page(slug, get_head(title, desc, slug) + f"""
        <main class="max-w-4xl mx-auto px-6 py-12">
            <h1 class="text-3xl md:text-5xl font-bold text-white mb-4">{f1['name']} vs {f2['name']}</h1>
            <p class="text-slate-300 mb-8">{desc}</p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div class="card-glow rounded-2xl p-6">
                    <h2 class="text-2xl font-bold text-cyan-400 mb-3">{f1['name']}</h2>
                    <ul class="text-sm space-y-2 text-slate-300">
                        <li><strong>Max Funding:</strong> {f1['max_alloc']}</li>
                        <li><strong>Drawdown:</strong> {f1['drawdown']}</li>
                        <li><strong>Split:</strong> {f1['split']}</li>
                        <li><strong>Code:</strong> <span class="mono text-amber-300">{f1['code']}</span></li>
                    </ul>
                </div>
                <div class="card-glow rounded-2xl p-6">
                    <h2 class="text-2xl font-bold text-emerald-400 mb-3">{f2['name']}</h2>
                    <ul class="text-sm space-y-2 text-slate-300">
                        <li><strong>Max Funding:</strong> {f2['max_alloc']}</li>
                        <li><strong>Drawdown:</strong> {f2['drawdown']}</li>
                        <li><strong>Split:</strong> {f2['split']}</li>
                        <li><strong>Code:</strong> <span class="mono text-amber-300">{f2['code']}</span></li>
                    </ul>
                </div>
            </div>
            <a href="/index.html#pricing" class="bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-extrabold px-6 py-3 rounded-xl text-sm">Equip NinjaTrader Bots &rarr;</a>
        </main>{PRICING_SECTION}""" + FOOTER_HTML)
        briefing_links.append((slug, title))

for b in BOTS:
    slug = f"bot-{b['slug']}.html"
    title = f"{b['name']} | NinjaTrader 8 C# Bot ({b['market']})"
    desc = f"{b['desc']} Backtested win rate: {b['win']}. Instant digital download for NinjaTrader 8."
    write_page(slug, get_head(title, desc, slug) + f"""
    <main class="max-w-4xl mx-auto px-6 py-12">
        <div class="mono text-xs text-cyan-400 mb-2">{b['market']} // BACKTEST WIN: {b['win']}</div>
        <h1 class="text-3xl md:text-5xl font-bold text-white mb-4">{b['name']}</h1>
        <p class="text-slate-300 text-lg mb-8">{b['desc']}</p>
        <div class="card-glow rounded-2xl p-8 flex flex-col md:flex-row justify-between items-center gap-6">
            <div>
                <div class="text-xs mono text-slate-400">INSTANT DIGITAL ACCESS</div>
                <div class="text-5xl font-black text-white mt-1">${b['price']}</div>
                <div class="text-xs text-emerald-400 mt-2">&#10003; Includes NinjaTrader 8 .zip file + ATM template</div>
            </div>
            <button onclick="checkout('{b['tier']}')" class="bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-black px-8 py-4 rounded-xl text-base shadow-[0_0_25px_rgba(0,255,157,0.3)]">
                Unlock Bot Now (${b['price']}) &rarr;
            </button>
        </div>
    </main>{PRICING_SECTION}""" + FOOTER_HTML)
    briefing_links.append((slug, title))

# 6. BRIEFINGS HUB (briefings.html)
links_html = "".join([f'<li class="py-2 border-b border-white/5"><a href="/{s}" class="text-cyan-400 hover:underline text-sm">{t}</a></li>' for s, t in briefing_links])
write_page("briefings.html", get_head("Complete Prop Firm & Algo Directory | The Funded Bible", "Direct crawlable directory of all prop firm audits and NinjaTrader 8 strategies.", "briefings.html") + f"""
<main class="max-w-4xl mx-auto px-6 py-12">
    <h1 class="text-3xl font-bold text-white mb-4">Complete Site Directory ({len(generated_urls)+1} Pages)</h1>
    <ul class="card-glow rounded-2xl p-6">{links_html}</ul>
</main>""" + FOOTER_HTML)

# 7. SITEMAP & ROBOTS
sitemap_items = "\n".join([f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>daily</changefreq><priority>0.9</priority></url>" for u in generated_urls])
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_items}\n</urlset>')
with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")

print(f"[SUCCESS] Compiled {len(generated_urls)} fully linked, payment-ready pages!")
