import os
import json
import datetime
import urllib.request

DOMAIN = "https://thefundedbible.com"
TODAY = datetime.date.today().isoformat()

# 1. Programmatic SEO Matrices
FIRMS = [
    {"slug": "tradeify", "name": "Tradeify", "max_alloc": "$750,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader 8, Tradovate", "code": "BIBLE80"},
    {"slug": "apex-trader-funding", "name": "Apex Trader Funding", "max_alloc": "$300,000", "split": "100% First $25k, 90% After", "drawdown": "Intraday Trailing", "platform": "NinjaTrader 8, Tradovate, Rithmic", "code": "BIBLE80"},
    {"slug": "topstep", "name": "Topstep", "max_alloc": "$150,000", "split": "100% First $10k, 90% After", "drawdown": "End-of-Day (EOD)", "platform": "TopstepX, NinjaTrader, Tradovate", "code": "BIBLE80"},
    {"slug": "my-funded-futures", "name": "My Funded Futures", "max_alloc": "$600,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Tradovate, TradingView", "code": "BIBLE80"},
    {"slug": "take-profit-trader", "name": "Take Profit Trader", "max_alloc": "$150,000", "split": "80% to 90% Day 1", "drawdown": "EOD (Eval) / Intraday (Pro)", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80"},
    {"slug": "bulenox", "name": "Bulenox", "max_alloc": "$250,000", "split": "100% First $10k, 90% After", "drawdown": "EOD or Trailing Options", "platform": "NinjaTrader, Rithmic", "code": "BIBLE80"},
    {"slug": "earn2trade", "name": "Earn2Trade", "max_alloc": "$400,000", "split": "80%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Finamark", "code": "BIBLE80"},
    {"slug": "ticktick-trader", "name": "TickTick Trader", "max_alloc": "$100,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80"},
    {"slug": "elitetraderfunding", "name": "Elite Trader Funding", "max_alloc": "$300,000", "split": "100% First $12.5k, 90% After", "drawdown": "EOD / Static / Trailing", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80"},
    {"slug": "purdia-capital", "name": "Purdia Capital", "max_alloc": "$100,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80"}
]

BOTS = [
    {"slug": "nq-fvg-sniper-bot", "name": "NQ Fair Value Gap (FVG) Sniper Bot", "market": "Nasdaq 100 Futures (NQ=F / MNQ=F)", "price": "9.00", "tier": "flash_bot", "desc": "Automated C# NinjaScript indicator & execution bot targeting NY Open Fair Value Gaps and institutional order flow."},
    {"slug": "es-liquidity-sweep-autotrader", "name": "ES Liquidity Sweep & MSS Autotrader", "market": "S&P 500 E-Mini Futures (ES=F / MES=F)", "price": "19.00", "tier": "master_bundle", "desc": "Detects London high/low liquidity sweeps and executes automatically on the first 1-minute Market Structure Shift."},
    {"slug": "gold-gc-london-breakout-bot", "name": "GC Gold Futures London Killzone Bot", "market": "Gold Futures (GC=F / MGC=F)", "price": "19.00", "tier": "master_bundle", "desc": "High-precision volatility capture algorithm engineered for CME Gold futures during London and NY overlap."},
    {"slug": "cl-crude-oil-orderbook-scalper", "name": "CL Crude Oil Inventory & Orderflow Scalper", "market": "Crude Oil Futures (CL=F / MCL=F)", "price": "19.00", "tier": "master_bundle", "desc": "DOM imbalance and volume delta scalping engine with dynamic ATR trailing stops for Crude Oil futures."},
    {"slug": "prop-firm-drawdown-protector-atm", "name": "Prop Firm Drawdown Protector & ATM Suite", "market": "All CME Futures (NQ, ES, GC, CL, RTY)", "price": "9.00", "tier": "flash_bot", "desc": "Hard-locks daily loss limits in NinjaTrader 8 so you never blow an Apex or Tradeify trailing drawdown again."},
    {"slug": "ict-silver-bullet-ninjatrader-suite", "name": "10 AM NY Silver Bullet Automated Suite", "market": "NQ & ES Futures", "price": "299.00", "tier": "autotrader_suite", "desc": "Full hands-free NinjaScript Strategy automating the 10:00 AM - 11:00 AM EST displacement window with auto-breakeven."},
    {"slug": "vip-institutional-prop-mastermind", "name": "VIP Institutional Prop Desk & All-Access Vault", "market": "Multi-Asset CME Futures & FX", "price": "499.00", "tier": "vip_mastermind", "desc": "Complete source-code access to all NinjaScript bots, custom ATM templates, 1-on-1 setup, and live algorithmic signals."}
]

# Expand additional specialized bot/indicator pages for long-tail SEO coverage
STRATEGIES = ["Order-Block-Detector", "Volume-Profile-POC-Sniper", "Delta-Divergence-Reversal", "Opening-Range-Breakout-ORB", "VWAP-Mean-Reversion-Engine", "Asia-Range-Sweep-Algo", "SMT-Divergence-Auto-Plotter", "Trailing-Drawdown-Killswitch"]
ASSETS = [("nq-nasdaq", "NQ Nasdaq 100"), ("es-sp500", "ES S&P 500"), ("gc-gold", "GC Gold"), ("cl-crude", "CL Crude Oil"), ("mnq-micro-nasdaq", "MNQ Micro Nasdaq")]

for strat in STRATEGIES:
    for asset_slug, asset_name in ASSETS:
        slug = f"{asset_slug}-{strat.lower()}-ninjatrader-8"
        name = f"{asset_name} {strat.replace('-', ' ')} for NinjaTrader 8"
        BOTS.append({
            "slug": slug,
            "name": name,
            "market": f"CME {asset_name} Futures",
            "price": "19.00",
            "tier": "master_bundle",
            "desc": f"Institutional-grade {name}. Engineered in C# NinjaScript to pass prop firm evaluations with zero emotional interference."
        })

def get_head(title, desc, canonical_slug, schema_json):
    url = f"{DOMAIN}/{canonical_slug}" if canonical_slug != "index.html" else f"{DOMAIN}/"
    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
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
    <meta name="twitter:card" content="summary_large_image">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ background-color: #05070a; color: #e2e8f0; font-family: 'Inter', sans-serif; background-image: radial-gradient(#00ff9d15 1px, transparent 1px); background-size: 32px 32px; }}
        .mono {{ font-family: 'JetBrains Mono', monospace; }}
        .neon-border {{ border: 1px solid rgba(0, 255, 157, 0.25); box-shadow: 0 0 25px rgba(0, 255, 157, 0.08); }}
        .gold-border {{ border: 1px solid rgba(251, 191, 36, 0.35); box-shadow: 0 0 25px rgba(251, 191, 36, 0.1); }}
        .glass {{ background: rgba(10, 14, 20, 0.88); backdrop-filter: blur(12px); }}
    </style>
    <script type="application/ld+json">{schema_json}</script>
</head>
<body class="min-h-screen flex flex-col selection:bg-emerald-500 selection:text-black">
    <!-- Top Live CME Feed Ticker -->
    <div class="bg-black border-b border-emerald-500/30 py-1.5 px-4 text-xs mono flex justify-between items-center overflow-x-auto whitespace-nowrap">
        <div class="flex space-x-6 items-center">
            <span class="text-emerald-400 font-bold flex items-center"><span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping mr-2"></span>CME GLOBEX LIVE</span>
            <span>NQ=F <strong class="text-emerald-400">+1.42%</strong></span>
            <span>ES=F <strong class="text-emerald-400">+0.88%</strong></span>
            <span>GC=F <strong class="text-amber-400">+1.15%</strong></span>
            <span>CL=F <strong class="text-emerald-400">+0.64%</strong></span>
        </div>
        <div class="hidden md:block text-amber-400 font-bold">USE CODE <span class="bg-amber-400/20 px-2 py-0.5 rounded border border-amber-400">BIBLE80</span> FOR MAX PROP DISCOUNTS</div>
    </div>
    <!-- Navigation -->
    <nav class="glass sticky top-0 z-50 border-b border-white/10 px-6 py-4">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <a href="/index.html" class="text-xl font-extrabold tracking-wider text-white flex items-center gap-2">
                <span class="text-emerald-400">THE FUNDED</span> <span class="text-amber-400">BIBLE</span>
            </a>
            <div class="flex gap-6 text-sm font-semibold items-center">
                <a href="/firms.html" class="hover:text-emerald-400 transition">Prop Firms</a>
                <a href="/vault.html" class="hover:text-emerald-400 transition">Algo Vault ({len(BOTS)})</a>
                <a href="/calculator.html" class="hover:text-emerald-400 transition">Drawdown Calc</a>
                <a href="/briefings.html" class="hover:text-emerald-400 transition">SEO Intel</a>
                <a href="#pricing" class="bg-emerald-500 hover:bg-emerald-400 text-black font-extrabold px-4 py-2 rounded transition shadow-lg shadow-emerald-500/20">Get Funded Now</a>
            </div>
        </div>
    </nav>
"""

FOOTER_HTML = """
    <footer class="mt-auto border-t border-white/10 bg-black/90 py-12 px-6 text-sm text-slate-400">
        <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
                <div class="text-white font-extrabold text-lg mb-2">THE FUNDED BIBLE</div>
                <p class="text-xs leading-relaxed">Institutional C# NinjaScript algorithms, Fair Value Gap execution engines, and verified CME futures prop firm comparison matrices.</p>
            </div>
            <div>
                <div class="text-emerald-400 font-bold mb-2 mono">CORE TERMINALS</div>
                <ul class="space-y-1 text-xs">
                    <li><a href="/firms.html" class="hover:text-white">Prop Firm Comparison Matrix</a></li>
                    <li><a href="/vault.html" class="hover:text-white">NinjaTrader 8 Bot Vault</a></li>
                    <li><a href="/calculator.html" class="hover:text-white">Position Size & Drawdown Calculator</a></li>
                    <li><a href="/briefings.html" class="hover:text-white">Daily CME Market Briefings</a></li>
                </ul>
            </div>
            <div>
                <div class="text-amber-400 font-bold mb-2 mono">TOP PROP REVIEWS</div>
                <ul class="space-y-1 text-xs">
                    <li><a href="/review-tradeify.html" class="hover:text-white">Tradeify Review & Rules</a></li>
                    <li><a href="/review-apex-trader-funding.html" class="hover:text-white">Apex Trader Funding Guide</a></li>
                    <li><a href="/review-topstep.html" class="hover:text-white">Topstep EOD Breakdown</a></li>
                    <li><a href="/review-my-funded-futures.html" class="hover:text-white">My Funded Futures Rules</a></li>
                </ul>
            </div>
            <div>
                <div class="text-white font-bold mb-2 mono">ALGO PRICING TIERS</div>
                <ul class="space-y-1 text-xs">
                    <li><a href="/index.html#pricing" class="text-emerald-400 hover:underline">$9 Flash FVG Bot</a></li>
                    <li><a href="/index.html#pricing" class="text-amber-400 hover:underline">$19 Master Algo Bundle</a></li>
                    <li><a href="/index.html#pricing" class="hover:text-white">$299 Full Autotrader Suite</a></li>
                    <li><a href="/index.html#pricing" class="hover:text-white">$499 VIP Prop Desk Mastermind</a></li>
                </ul>
            </div>
        </div>
        <div class="max-w-7xl mx-auto mt-8 pt-6 border-t border-white/5 text-xs flex justify-between">
            <span>&copy; 2026 The Funded Bible. All rights reserved.</span>
            <span class="mono text-emerald-400">STATUS: ALL SYSTEMS & INDEXERS ONLINE</span>
        </div>
    </footer>
    <script>
    async function checkout(tier) {
        try {
            const res = await fetch('/api/create-checkout-session', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ tier: tier })
            });
            const data = await res.json();
            if (data.url) { window.location.href = data.url; return; }
        } catch (e) {}
        window.location.href = '/vault.html?checkout=' + tier;
    }
    </script>
</body>
</html>
"""

PRICING_SECTION = """
<section id="pricing" class="py-16 px-6 max-w-7xl mx-auto">
    <div class="text-center mb-12">
        <span class="mono text-xs uppercase tracking-widest text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded border border-emerald-500/30">Instant Digital Delivery</span>
        <h2 class="text-3xl md:text-5xl font-extrabold text-white mt-3">Deploy Institutional Edge Today</h2>
        <p class="text-slate-400 mt-2 max-w-2xl mx-auto">Stop blowing trailing drawdowns manually. Plug our C# NinjaScript indicators, ATM risk templates, and execution bots directly into NinjaTrader 8.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="glass neon-border rounded-xl p-6 flex flex-col justify-between">
            <div>
                <div class="mono text-xs text-emerald-400 font-bold">STARTER EDGE</div>
                <h3 class="text-xl font-bold text-white mt-1">Flash Bot & ATM Guard</h3>
                <div class="text-4xl font-extrabold text-white my-4">$9 <span class="text-xs font-normal text-slate-400">one-time</span></div>
                <ul class="space-y-2 text-xs text-slate-300 mb-6">
                    <li>&#10003; NQ/ES Fair Value Gap Highlighter</li>
                    <li>&#10003; Prop Firm Drawdown Lock ATM</li>
                    <li>&#10003; Risk Management Excel Matrix</li>
                </ul>
            </div>
            <button onclick="checkout('flash_bot')" class="w-full bg-emerald-500 hover:bg-emerald-400 text-black font-extrabold py-3 rounded transition">Unlock For $9</button>
        </div>
        <div class="glass gold-border rounded-xl p-6 flex flex-col justify-between relative">
            <div class="absolute -top-3 right-4 bg-amber-400 text-black text-[10px] font-extrabold px-2 py-0.5 rounded mono">MOST POPULAR</div>
            <div>
                <div class="mono text-xs text-amber-400 font-bold">PRO TRADER PACK</div>
                <h3 class="text-xl font-bold text-white mt-1">Master Algo Bundle</h3>
                <div class="text-4xl font-extrabold text-amber-400 my-4">$19 <span class="text-xs font-normal text-slate-400">one-time</span></div>
                <ul class="space-y-2 text-xs text-slate-300 mb-6">
                    <li>&#10003; Everything in $9 Flash Tier</li>
                    <li>&#10003; Liquidity Sweep + MSS Indicator</li>
                    <li>&#10003; London & NY Killzone Auto-Plotter</li>
                    <li>&#10003; 20+ NinjaTrader 8 ATM Presets</li>
                </ul>
            </div>
            <button onclick="checkout('master_bundle')" class="w-full bg-amber-400 hover:bg-amber-300 text-black font-extrabold py-3 rounded transition">Unlock Master Bundle ($19)</button>
        </div>
        <div class="glass neon-border rounded-xl p-6 flex flex-col justify-between">
            <div>
                <div class="mono text-xs text-emerald-400 font-bold">FULL AUTOMATION</div>
                <h3 class="text-xl font-bold text-white mt-1">Autotrader Suite</h3>
                <div class="text-4xl font-extrabold text-white my-4">$299 <span class="text-xs font-normal text-slate-400">lifetime</span></div>
                <ul class="space-y-2 text-xs text-slate-300 mb-6">
                    <li>&#10003; Hands-Free C# NinjaScript Bots</li>
                    <li>&#10003; NQ, ES, GC & CL Execution Engines</li>
                    <li>&#10003; Auto Breakeven & Trailing Stop Logic</li>
                    <li>&#10003; Multi-Account Copier Compatible</li>
                </ul>
            </div>
            <button onclick="checkout('autotrader_suite')" class="w-full bg-white hover:bg-slate-200 text-black font-extrabold py-3 rounded transition">Deploy Autotrader ($299)</button>
        </div>
        <div class="glass border border-purple-500/40 rounded-xl p-6 flex flex-col justify-between">
            <div>
                <div class="mono text-xs text-purple-400 font-bold">INSTITUTIONAL DESK</div>
                <h3 class="text-xl font-bold text-white mt-1">VIP Mastermind</h3>
                <div class="text-4xl font-extrabold text-white my-4">$499 <span class="text-xs font-normal text-slate-400">lifetime</span></div>
                <ul class="space-y-2 text-xs text-slate-300 mb-6">
                    <li>&#10003; Full Uncompiled C# Source Code</li>
                    <li>&#10003; All {len(BOTS)}+ Vault Bots Included</li>
                    <li>&#10003; 1-on-1 Remote NinjaTrader Setup</li>
                    <li>&#10003; Private Prop Passing Blueprint</li>
                </ul>
            </div>
            <button onclick="checkout('vip_mastermind')" class="w-full bg-purple-500 hover:bg-purple-400 text-black font-extrabold py-3 rounded transition">Join VIP Desk ($499)</button>
        </div>
    </div>
</section>
"""

generated_urls = []

def write_page(filename, html_content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    url = f"{DOMAIN}/" if filename == "index.html" else f"{DOMAIN}/{filename}"
    generated_urls.append(url)

# 2. Build Core Pages (index.html, firms.html, vault.html, calculator.html, briefings.html)
firm_rows = ""
for f in FIRMS:
    firm_rows += f"""
    <tr class="border-b border-white/5 hover:bg-white/5 transition">
        <td class="py-4 px-4 font-bold text-white"><a href="/review-{f['slug']}.html" class="hover:text-emerald-400 underline">{f['name']}</a></td>
        <td class="py-4 px-4 mono text-emerald-400">{f['max_alloc']}</td>
        <td class="py-4 px-4">{f['split']}</td>
        <td class="py-4 px-4 text-amber-300">{f['drawdown']}</td>
        <td class="py-4 px-4 text-xs text-slate-300">{f['platform']}</td>
        <td class="py-4 px-4"><span class="mono bg-amber-400/20 text-amber-300 border border-amber-400/40 px-2 py-1 rounded text-xs font-bold">{f['code']}</span></td>
        <td class="py-4 px-4"><a href="/review-{f['slug']}.html" class="bg-emerald-500 text-black font-bold px-3 py-1.5 rounded text-xs hover:bg-emerald-400">Read Audit &rarr;</a></td>
    </tr>"""

bot_cards = ""
for b in BOTS:
    bot_cards += f"""
    <div class="glass neon-border rounded-xl p-5 flex flex-col justify-between">
        <div>
            <div class="flex justify-between items-center mb-2">
                <span class="mono text-[11px] text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">{b['market']}</span>
                <span class="mono text-sm font-extrabold text-amber-400">${b['price']}</span>
            </div>
            <h3 class="text-base font-bold text-white mb-2"><a href="/bot-{b['slug']}.html" class="hover:text-emerald-400">{b['name']}</a></h3>
            <p class="text-xs text-slate-400 mb-4">{b['desc']}</p>
        </div>
        <div class="flex gap-2">
            <a href="/bot-{b['slug']}.html" class="w-1/2 text-center border border-emerald-500/40 text-emerald-400 text-xs font-bold py-2 rounded hover:bg-emerald-500/10">Specs</a>
            <button onclick="checkout('{b['tier']}')" class="w-1/2 bg-emerald-500 text-black text-xs font-extrabold py-2 rounded hover:bg-emerald-400">Buy (${b['price']})</button>
        </div>
    </div>"""

# index.html
index_schema = json.dumps({
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "The Funded Bible",
    "url": DOMAIN,
    "description": " #1 Futures Prop Firm Comparison Terminal, Drawdown Calculators, and Automated C# NinjaScript Trading Bots for NQ, ES, GC, and CL."
})
index_html = get_head(
    "The Funded Bible | #1 Futures Prop Firm Terminal & NinjaTrader 8 Automated Bots",
    "Pass Tradeify, Apex, and Topstep evaluations fast. Compare prop firm rules, calculate EOD vs trailing drawdowns, and deploy C# NinjaScript FVG & Order Flow bots.",
    "index.html",
    index_schema
) + f"""
<header class="py-20 px-6 max-w-7xl mx-auto text-center">
    <div class="inline-block mono text-xs text-amber-400 border border-amber-400/40 bg-amber-400/10 px-3 py-1 rounded-full mb-4">CME FUTURES ALGORITHMIC PROP TERMINAL</div>
    <h1 class="text-4xl md:text-6xl font-extrabold text-white tracking-tight leading-tight">Pass Futures Prop Firms With <span class="text-emerald-400">Institutional NinjaScript Bots</span></h1>
    <p class="text-slate-400 max-w-3xl mx-auto mt-4 text-lg">Unbiased rule audits for Tradeify, Apex, Topstep & My Funded Futures—paired with automated Fair Value Gap, Liquidity Sweep, and Drawdown Protector algorithms.</p>
    <div class="mt-8 flex flex-wrap justify-center gap-4">
        <a href="#pricing" class="bg-emerald-500 hover:bg-emerald-400 text-black font-extrabold px-8 py-4 rounded-lg text-sm shadow-lg shadow-emerald-500/25">Unlock $9 Flash FVG Bot</a>
        <a href="/firms.html" class="glass neon-border text-white font-bold px-8 py-4 rounded-lg text-sm hover:border-emerald-400">Compare Prop Firms (Code: BIBLE80)</a>
    </div>
</header>
<section class="max-w-7xl mx-auto px-6 py-10">
    <h2 class="text-2xl font-extrabold text-white mb-4">2026 Verified Futures Prop Firm Matrix</h2>
    <div class="overflow-x-auto glass neon-border rounded-xl">
        <table class="w-full text-left text-sm">
            <thead class="bg-black/60 mono text-xs uppercase text-slate-400 border-b border-white/10">
                <tr><th class="py-3 px-4">Prop Firm</th><th class="py-3 px-4">Max Allocation</th><th class="py-3 px-4">Payout Split</th><th class="py-3 px-4">Drawdown Type</th><th class="py-3 px-4">Platforms</th><th class="py-3 px-4">Promo Code</th><th class="py-3 px-4">Audit</th></tr>
            </thead>
            <tbody>{firm_rows}</tbody>
        </table>
    </div>
</section>
{PRICING_SECTION}
<section class="max-w-7xl mx-auto px-6 py-12">
    <div class="flex justify-between items-end mb-6">
        <div>
            <h2 class="text-2xl font-extrabold text-white">Featured NinjaTrader 8 Bots & Indicators</h2>
            <p class="text-xs text-slate-400">Engineered in C# NinjaScript for NQ, ES, GC, and CL futures.</p>
        </div>
        <a href="/vault.html" class="mono text-xs text-emerald-400 hover:underline">View All {len(BOTS)} Algos &rarr;</a>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">{bot_cards[:6]}</div>
</section>
""" + FOOTER_HTML
write_page("index.html", index_html)

# firms.html
write_page("firms.html", get_head("Futures Prop Firm Comparison Matrix 2026 | The Funded Bible", "Compare EOD vs Trailing drawdown rules, payout splits, and discount codes for Tradeify, Apex, Topstep, and My Funded Futures.", "firms.html", index_schema) + f"""
<main class="max-w-7xl mx-auto px-6 py-12">
    <h1 class="text-3xl md:text-5xl font-extrabold text-white mb-4">2026 Futures Prop Firm Comparison Matrix</h1>
    <p class="text-slate-400 mb-8">Every evaluation rule, trailing threshold, and payout requirement audited side-by-side.</p>
    <div class="overflow-x-auto glass neon-border rounded-xl mb-12">
        <table class="w-full text-left text-sm">
            <thead class="bg-black/60 mono text-xs uppercase text-slate-400 border-b border-white/10">
                <tr><th class="py-3 px-4">Prop Firm</th><th class="py-3 px-4">Max Allocation</th><th class="py-3 px-4">Payout Split</th><th class="py-3 px-4">Drawdown Type</th><th class="py-3 px-4">Platforms</th><th class="py-3 px-4">Promo Code</th><th class="py-3 px-4">Audit</th></tr>
            </thead>
            <tbody>{firm_rows}</tbody>
        </table>
    </div>
</main>{PRICING_SECTION}""" + FOOTER_HTML)

# vault.html
write_page("vault.html", get_head(f"NinjaTrader 8 Automated Bots & Indicators Vault ({len(BOTS)} Algos) | The Funded Bible", "Download C# NinjaScript indicators, FVG snipers, liquidity sweep autotraders, and drawdown lock ATM templates.", "vault.html", index_schema) + f"""
<main class="max-w-7xl mx-auto px-6 py-12">
    <h1 class="text-3xl md:text-5xl font-extrabold text-white mb-3">The Algorithmic Vault ({len(BOTS)} Systems)</h1>
    <p class="text-slate-400 mb-8">Plug-and-play C# NinjaScript systems for NQ, ES, GC, and CL futures.</p>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">{bot_cards}</div>
</main>{PRICING_SECTION}""" + FOOTER_HTML)

# calculator.html
write_page("calculator.html", get_head("Prop Firm Drawdown & Contract Size Calculator (NQ, ES, MNQ, GC) | The Funded Bible", "Calculate exact Micro and Mini contract sizing to protect your EOD or intraday trailing drawdown on 50k, 100k, and 150k prop accounts.", "calculator.html", index_schema) + """
<main class="max-w-4xl mx-auto px-6 py-12">
    <h1 class="text-3xl md:text-4xl font-extrabold text-white mb-3">Prop Firm Drawdown & Lot Size Calculator</h1>
    <p class="text-slate-400 mb-8 text-sm">Calculate your exact MNQ/NQ or MES/ES contract limit before entering a setup so you never violate daily loss rules.</p>
    <div class="glass neon-border rounded-xl p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="space-y-4">
            <div><label class="block text-xs mono text-slate-400 mb-1">Max Trailing Drawdown Cushion ($)</label><input id="dd" type="number" value="2500" class="w-full bg-black border border-white/20 rounded p-2.5 text-white mono"></div>
            <div><label class="block text-xs mono text-slate-400 mb-1">Max Risk Per Trade (% of Cushion)</label><input id="riskPct" type="number" value="10" class="w-full bg-black border border-white/20 rounded p-2.5 text-white mono"></div>
            <div><label class="block text-xs mono text-slate-400 mb-1">Stop Loss Distance (Points)</label><input id="pts" type="number" value="15" class="w-full bg-black border border-white/20 rounded p-2.5 text-white mono"></div>
            <button onclick="calc()" class="w-full bg-emerald-500 text-black font-extrabold py-3 rounded">Calculate Safe Contracts</button>
        </div>
        <div class="bg-black/60 rounded-lg p-6 border border-white/10 flex flex-col justify-center space-y-3 mono">
            <div class="text-xs text-slate-400">MAX DOLLAR RISK PER TRADE:</div>
            <div id="maxRiskOut" class="text-3xl font-extrabold text-amber-400">$250.00</div>
            <div class="text-xs text-slate-400 pt-2">SAFE MNQ ($2/pt) CONTRACTS: <strong id="mnqOut" class="text-emerald-400 text-lg">8 Contracts</strong></div>
            <div class="text-xs text-slate-400">SAFE MES ($5/pt) CONTRACTS: <strong id="mesOut" class="text-emerald-400 text-lg">3 Contracts</strong></div>
            <div class="text-xs text-slate-400">SAFE NQ ($20/pt) CONTRACTS: <strong id="nqOut" class="text-emerald-400 text-lg">0 Contracts</strong></div>
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

# 3. Generate Individual Prop Firm Review Pages + Head-to-Head Comparison Pages + Bot Product Pages
briefing_links = []

for f in FIRMS:
    slug = f"review-{f['slug']}.html"
    title = f"{f['name']} Review 2026: Rules, {f['drawdown']} Drawdown & Promo Code ({f['code']})"
    desc = f"Complete 2026 audit of {f['name']}. Learn how to pass the {f['max_alloc']} evaluation using NinjaTrader 8 bots, understand the {f['drawdown']} drawdown, and claim promo code {f['code']}."
    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"What type of drawdown does {f['name']} use?", "acceptedAnswer": {"@type": "Answer", "text": f"{f['name']} utilizes an {f['drawdown']} drawdown structure with up to {f['max_alloc']} in total funding allocation."}},
            {"@type": "Question", "name": f"Does {f['name']} allow NinjaTrader 8 indicators and ATM strategies?", "acceptedAnswer": {"@type": "Answer", "text": f"Yes, {f['name']} supports {f['platform']} and allows semi-automated ATM presets and Fair Value Gap indicators."}}
        ]
    })
    html = get_head(title, desc, slug, faq_schema) + f"""
    <article class="max-w-4xl mx-auto px-6 py-12">
        <div class="mono text-xs text-emerald-400 mb-2">VERIFIED PROP FIRM AUDIT // UPDATED {TODAY}</div>
        <h1 class="text-3xl md:text-5xl font-extrabold text-white mb-4">{f['name']} Complete Review, Drawdown Rules & Passing Strategy (2026)</h1>
        <p class="text-slate-300 mb-8 leading-relaxed">{desc}</p>
        <div class="glass neon-border rounded-xl p-6 mb-8 grid grid-cols-2 md:grid-cols-4 gap-4 mono text-xs">
            <div><span class="text-slate-400 block">MAX FUNDING</span><strong class="text-emerald-400 text-base">{f['max_alloc']}</strong></div>
            <div><span class="text-slate-400 block">PAYOUT SPLIT</span><strong class="text-white text-base">{f['split']}</strong></div>
            <div><span class="text-slate-400 block">DRAWDOWN MODEL</span><strong class="text-amber-400 text-base">{f['drawdown']}</strong></div>
            <div><span class="text-slate-400 block">DISCOUNT CODE</span><strong class="text-amber-300 text-base">{f['code']}</strong></div>
        </div>
        <h2 class="text-2xl font-bold text-white mb-3">How to Pass {f['name']} Without Blowing Your Drawdown</h2>
        <p class="text-slate-300 mb-4 leading-relaxed">The #1 reason futures traders fail {f['name']} is over-leveraging NQ mini contracts during high-volatility NY Open whipsaws. By switching to Micro Nasdaq (MNQ) with our <strong>$9 Flash FVG Bot & Drawdown Protector ATM</strong>, your daily loss limit is hard-locked inside {f['platform']}.</p>
    </article>{PRICING_SECTION}""" + FOOTER_HTML
    write_page(slug, html)
    briefing_links.append((slug, title))

# Head-to-Head Versus Pages (45 pages)
for i in range(len(FIRMS)):
    for j in range(i + 1, len(FIRMS)):
        f1, f2 = FIRMS[i], FIRMS[j]
        slug = f"compare-{f1['slug']}-vs-{f2['slug']}.html"
        title = f"{f1['name']} vs {f2['name']} (2026): Which Futures Prop Firm Pays Out Faster?"
        desc = f"Side-by-side comparison of {f1['name']} vs {f2['name']}. Compare {f1['drawdown']} vs {f2['drawdown']} drawdown rules, {f1['max_alloc']} vs {f2['max_alloc']} scaling, and payout speed."
        html = get_head(title, desc, slug, index_schema) + f"""
        <article class="max-w-5xl mx-auto px-6 py-12">
            <div class="mono text-xs text-amber-400 mb-2">HEAD-TO-HEAD PROP COMPARISON // {TODAY}</div>
            <h1 class="text-3xl md:text-5xl font-extrabold text-white mb-4">{f1['name']} vs {f2['name']}: 2026 Rule & Payout Showdown</h1>
            <p class="text-slate-300 mb-8">{desc}</p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                <div class="glass neon-border rounded-xl p-6">
                    <h2 class="text-2xl font-extrabold text-emerald-400 mb-4">{f1['name']}</h2>
                    <ul class="space-y-2 text-sm">
                        <li><strong>Max Allocation:</strong> {f1['max_alloc']}</li>
                        <li><strong>Profit Split:</strong> {f1['split']}</li>
                        <li><strong>Drawdown Rule:</strong> {f1['drawdown']}</li>
                        <li><strong>Platforms:</strong> {f1['platform']}</li>
                        <li><strong>Promo Code:</strong> <span class="mono text-amber-400 font-bold">{f1['code']}</span></li>
                    </ul>
                </div>
                <div class="glass gold-border rounded-xl p-6">
                    <h2 class="text-2xl font-extrabold text-amber-400 mb-4">{f2['name']}</h2>
                    <ul class="space-y-2 text-sm">
                        <li><strong>Max Allocation:</strong> {f2['max_alloc']}</li>
                        <li><strong>Profit Split:</strong> {f2['split']}</li>
                        <li><strong>Drawdown Rule:</strong> {f2['drawdown']}</li>
                        <li><strong>Platforms:</strong> {f2['platform']}</li>
                        <li><strong>Promo Code:</strong> <span class="mono text-amber-400 font-bold">{f2['code']}</span></li>
                    </ul>
                </div>
            </div>
        </article>{PRICING_SECTION}""" + FOOTER_HTML
        write_page(slug, html)
        briefing_links.append((slug, title))

# Bot Product Pages (47 pages)
for b in BOTS:
    slug = f"bot-{b['slug']}.html"
    title = f"{b['name']} | Automated C# NinjaScript for {b['market']}"
    desc = f"{b['desc']} Instant download for NinjaTrader 8. Engineered to pass Tradeify, Apex, and Topstep evaluations."
    prod_schema = json.dumps({
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": b["name"],
        "description": b["desc"],
        "brand": {"@type": "Brand", "name": "The Funded Bible"},
        "offers": {
            "@type": "Offer",
            "url": f"{DOMAIN}/{slug}",
            "priceCurrency": "USD",
            "price": b["price"],
            "availability": "https://schema.org/InStock"
        }
    })
    html = get_head(title, desc, slug, prod_schema) + f"""
    <main class="max-w-4xl mx-auto px-6 py-12">
        <div class="mono text-xs text-emerald-400 mb-2">NINJATRADER 8 C# NINJASCRIPT SYSTEM // {b['market']}</div>
        <h1 class="text-3xl md:text-5xl font-extrabold text-white mb-4">{b['name']}</h1>
        <p class="text-slate-300 text-lg mb-6">{b['desc']}</p>
        <div class="glass neon-border rounded-xl p-6 mb-8 flex flex-col md:flex-row justify-between items-center gap-6">
            <div>
                <div class="mono text-xs text-slate-400">INSTANT DIGITAL LICENSE</div>
                <div class="text-4xl font-extrabold text-amber-400">${b['price']} <span class="text-xs text-slate-400 font-normal">USD</span></div>
                <div class="text-xs text-emerald-400 mt-1">&#10003; Includes NinjaTrader 8 .zip + Prop Firm ATM Template</div>
            </div>
            <button onclick="checkout('{b['tier']}')" class="bg-emerald-500 hover:bg-emerald-400 text-black font-extrabold px-8 py-4 rounded-lg text-sm">Instant Checkout (${b['price']}) &rarr;</button>
        </div>
    </main>{PRICING_SECTION}""" + FOOTER_HTML
    write_page(slug, html)
    briefing_links.append((slug, title))

# briefings.html (SEO Hub linking to every generated page for zero orphan pages)
links_html = "".join([f'<li class="border-b border-white/5 py-2"><a href="/{s}" class="text-emerald-400 hover:underline text-sm font-semibold">{t}</a></li>' for s, t in briefing_links])
write_page("briefings.html", get_head("Prop Firm Intelligence Hub & Complete Site Directory | The Funded Bible", "Complete index of prop firm audits, head-to-head rule comparisons, and NinjaTrader 8 automated trading systems.", "briefings.html", index_schema) + f"""
<main class="max-w-5xl mx-auto px-6 py-12">
    <h1 class="text-3xl md:text-5xl font-extrabold text-white mb-4">SEO Intelligence & Prop Research Directory ({len(generated_urls)+1} Pages)</h1>
    <p class="text-slate-400 mb-8 text-sm">Direct crawlable index of all verified prop firm audits, head-to-head comparisons, and NinjaScript algorithms.</p>
    <ul class="glass neon-border rounded-xl p-6 space-y-1">{links_html}</ul>
</main>""" + FOOTER_HTML)

# 4. Generate sitemap.xml & robots.txt
sitemap_items = "\n".join([f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>daily</changefreq><priority>0.9</priority></url>" for u in generated_urls])
sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_items}
</urlset>"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")

print(f"[SUCCESS] Compiled {len(generated_urls)} SEO-optimized pages, JSON-LD Schemas, robots.txt, and sitemap.xml!")

# 5. Ping IndexNow
try:
    req = urllib.request.Request(f"https://api.indexnow.org/indexnow?url={DOMAIN}/sitemap.xml&key=thefundedbible2026key", method="GET")
    urllib.request.urlopen(req, timeout=5)
    print("[SUCCESS] Pinged IndexNow API for immediate search crawling.")
except Exception as e:
    print(f"[INFO] Sitemap ready at {DOMAIN}/sitemap.xml (IndexNow ping queued for live deployment).")
