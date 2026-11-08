import os
import json
import datetime

DOMAIN = "https://thefundedbible.com"
TODAY = datetime.date.today().isoformat()

FIRMS = [
    {"slug": "tradeify", "name": "Tradeify", "max_alloc": "$750,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader 8, Tradovate", "code": "BIBLE80"},
    {"slug": "apex-trader-funding", "name": "Apex Trader Funding", "max_alloc": "$300,000", "split": "100% First $25k / 90% After", "drawdown": "Intraday Trailing", "platform": "NinjaTrader 8, Tradovate, Rithmic", "code": "BIBLE80"},
    {"slug": "topstep", "name": "Topstep", "max_alloc": "$150,000", "split": "100% First $10k / 90% After", "drawdown": "End-of-Day (EOD)", "platform": "TopstepX, NinjaTrader 8", "code": "BIBLE80"},
    {"slug": "my-funded-futures", "name": "My Funded Futures", "max_alloc": "$600,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Tradovate, TradingView", "code": "BIBLE80"},
    {"slug": "take-profit-trader", "name": "Take Profit Trader", "max_alloc": "$150,000", "split": "80% to 90% Day 1", "drawdown": "EOD (Eval) / Intraday (Pro)", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80"},
    {"slug": "bulenox", "name": "Bulenox", "max_alloc": "$250,000", "split": "100% First $10k / 90% After", "drawdown": "EOD or Trailing Options", "platform": "NinjaTrader, Rithmic", "code": "BIBLE80"},
    {"slug": "earn2trade", "name": "Earn2Trade", "max_alloc": "$400,000", "split": "80%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Finamark", "code": "BIBLE80"},
    {"slug": "ticktick-trader", "name": "TickTick Trader", "max_alloc": "$100,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80"},
    {"slug": "elitetraderfunding", "name": "Elite Trader Funding", "max_alloc": "$300,000", "split": "100% First $12.5k / 90% After", "drawdown": "EOD / Static / Trailing", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80"},
    {"slug": "purdia-capital", "name": "Purdia Capital", "max_alloc": "$100,000", "split": "90%", "drawdown": "End-of-Day (EOD)", "platform": "NinjaTrader, Tradovate", "code": "BIBLE80"}
]

BOTS = [
    {"slug": "nq-fvg-sniper-bot", "name": "NQ Fair Value Gap Sniper", "cat": "nq", "market": "NQ / MNQ Futures", "win": "78.4%", "price": "9", "tier": "flash_bot", "badge": "BESTSELLER", "desc": "C# NinjaScript indicator & execution bot targeting NY Open Fair Value Gaps and institutional order flow with hard-locked prop drawdown limits."},
    {"slug": "prop-firm-drawdown-protector-atm", "name": "Trailing Drawdown Killswitch", "cat": "risk", "market": "All CME Futures", "win": "100% Rule Lock", "price": "9", "tier": "flash_bot", "badge": "ESSENTIAL", "desc": "Automatically flattens open contracts and locks NinjaTrader 8 when you reach 80% of your daily max loss to protect your evaluation."},
    {"slug": "es-liquidity-sweep-autotrader", "name": "ES Liquidity Sweep + MSS Bot", "cat": "es", "market": "ES / MES Futures", "win": "74.1%", "price": "19", "tier": "master_bundle", "badge": "PRO PICK", "desc": "Detects London session high and low sweeps and enters automatically on the first confirmed 1-minute Market Structure Shift."},
    {"slug": "gold-gc-london-breakout-bot", "name": "GC Gold Killzone Sniper", "cat": "gold", "market": "GC / MGC Gold", "win": "76.8%", "price": "19", "tier": "master_bundle", "badge": "HIGH RR", "desc": "Captures 8:20 AM CME Gold volatility with automated multi-target runner management and dynamic trailing stops."},
    {"slug": "ict-silver-bullet-ninjatrader-suite", "name": "10 AM Silver Bullet Autotrader", "cat": "nq", "market": "NQ & ES Futures", "win": "81.2%", "price": "299", "tier": "autotrader_suite", "badge": "FULL AUTO", "desc": "100% hands-free C# strategy automating the 10:00 AM - 11:00 AM EST displacement window with automated break-even protection."},
    {"slug": "vip-institutional-prop-mastermind", "name": "All-Access Institutional Vault", "cat": "risk", "market": "Multi-Asset Desk", "win": "All 102 Bots", "price": "499", "tier": "vip_mastermind", "badge": "VIP DESK", "desc": "Uncompiled C# source code to every bot, custom ATM templates, 1-on-1 remote NinjaTrader setup, and private algorithmic signal channel."}
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
            "desc": f"Plug-and-play C# NinjaScript {clean_title} engineered for NinjaTrader 8 with strict prop-firm drawdown safeguards."
        })

def get_head(title, desc, canonical_slug, schema_json):
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
            background: rgba(10, 15, 24, 0.85);
            border: 1px solid rgba(0, 242, 254, 0.18);
            transition: all 0.25s ease;
        }}
        .card-glow:hover {{
            border-color: rgba(0, 255, 157, 0.6);
            transform: translateY(-4px);
            box-shadow: 0 12px 35px -10px rgba(0, 255, 157, 0.22);
        }}
    </style>
    <script type="application/ld+json">{schema_json}</script>
</head>
<body class="min-h-screen flex flex-col selection:bg-cyan-400 selection:text-black">
    <!-- Live CME Ticker Bar -->
    <div class="bg-[#020305] border-b border-cyan-500/20 py-2 px-6 text-xs mono flex justify-between items-center">
        <div class="flex items-center space-x-6 overflow-x-auto whitespace-nowrap">
            <span class="text-cyan-400 font-bold flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>CME GLOBEX</span>
            <span>NQ=F <strong id="tick-nq" class="text-emerald-400">21,452.50 (+1.42%)</strong></span>
            <span>ES=F <strong id="tick-es" class="text-emerald-400">6,024.75 (+0.88%)</strong></span>
            <span>GC=F <strong id="tick-gc" class="text-amber-300">2,684.20 (+1.15%)</strong></span>
            <span>CL=F <strong id="tick-cl" class="text-emerald-400">70.42 (+0.64%)</strong></span>
        </div>
        <div class="hidden sm:block text-slate-300">
            PROP CODE: <span class="text-amber-300 font-bold bg-amber-400/10 border border-amber-400/30 px-2 py-0.5 rounded ml-1">BIBLE80</span>
        </div>
    </div>

    <!-- Navigation -->
    <nav class="sticky top-0 z-50 bg-[#030508]/90 backdrop-blur-md border-b border-white/10 px-6 py-4">
        <div class="max-w-6xl mx-auto flex justify-between items-center">
            <a href="/index.html" class="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
                <span class="w-3 h-3 rounded-sm bg-gradient-to-tr from-cyan-400 to-emerald-400"></span>
                THE FUNDED <span class="text-cyan-400">BIBLE</span>
            </a>
            <div class="hidden md:flex gap-8 text-sm font-semibold text-slate-300">
                <a href="/index.html#bots" class="hover:text-cyan-400 transition">Featured Bots</a>
                <a href="/firms.html" class="hover:text-cyan-400 transition">Prop Firms (10)</a>
                <a href="/calculator.html" class="hover:text-cyan-400 transition">Lot Calculator</a>
                <a href="/vault.html" class="hover:text-cyan-400 transition">Full Vault ({len(BOTS)})</a>
                <a href="/briefings.html" class="hover:text-cyan-400 transition">Site Directory</a>
            </div>
            <a href="/index.html#pricing" class="bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-extrabold text-xs md:text-sm px-5 py-2.5 rounded-lg shadow-lg shadow-cyan-500/20 hover:opacity-95 transition">
                Unlock Bots &rarr;
            </a>
        </div>
    </nav>
"""

PRICING_SECTION = f"""
<section id="pricing" class="py-16 px-6 max-w-6xl mx-auto">
    <div class="text-center mb-12">
        <div class="mono text-xs text-cyan-400 uppercase tracking-widest mb-2">INSTANT DIGITAL ACCESS // NO SUBSCRIPTIONS</div>
        <h2 class="text-3xl md:text-5xl font-bold text-white">Select Your Algorithmic Edge</h2>
        <p class="text-slate-400 mt-2">Engineered specifically to pass Tradeify, Apex, Topstep, and My Funded Futures.</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="card-glow rounded-2xl p-6 flex flex-col justify-between">
            <div>
                <div class="mono text-xs text-cyan-400 font-bold">STARTER EDGE</div>
                <h3 class="text-xl font-bold text-white mt-1">Flash FVG Bot</h3>
                <div class="text-4xl font-black text-white my-4">$9 <span class="text-xs font-normal text-slate-400">one-time</span></div>
                <ul class="text-xs text-slate-300 space-y-2 mb-6">
                    <li>&#10003; NQ & ES Fair Value Gap Indicator</li>
                    <li>&#10003; Trailing Drawdown Killswitch ATM</li>
                    <li>&#10003; Instant NinjaTrader 8 .zip File</li>
                </ul>
            </div>
            <button onclick="checkout('flash_bot')" class="w-full bg-white/10 hover:bg-cyan-400 hover:text-black text-white font-bold py-3 rounded-xl transition">Unlock For $9</button>
        </div>

        <div class="card-glow rounded-2xl p-6 flex flex-col justify-between border-2 border-emerald-400 relative shadow-[0_0_40px_rgba(0,255,157,0.15)]">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-cyan-400 to-emerald-400 text-black text-[11px] font-black px-3 py-0.5 rounded-full mono">MOST POPULAR</div>
            <div>
                <div class="mono text-xs text-emerald-400 font-bold">PRO TRADER PACK</div>
                <h3 class="text-xl font-bold text-white mt-1">Master Bundle</h3>
                <div class="text-4xl font-black text-emerald-400 my-4">$19 <span class="text-xs font-normal text-slate-400">one-time</span></div>
                <ul class="text-xs text-slate-300 space-y-2 mb-6">
                    <li>&#10003; Everything in $9 Starter Pack</li>
                    <li>&#10003; Liquidity Sweep + MSS Autotrader</li>
                    <li>&#10003; London & NY Killzone Auto-Plotter</li>
                    <li>&#10003; 20+ Prop Firm ATM Templates</li>
                </ul>
            </div>
            <button onclick="checkout('master_bundle')" class="w-full bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-black py-3 rounded-xl transition">Get Master Pack ($19)</button>
        </div>

        <div class="card-glow rounded-2xl p-6 flex flex-col justify-between">
            <div>
                <div class="mono text-xs text-cyan-400 font-bold">HANDS-FREE</div>
                <h3 class="text-xl font-bold text-white mt-1">Autotrader Suite</h3>
                <div class="text-4xl font-black text-white my-4">$299 <span class="text-xs font-normal text-slate-400">lifetime</span></div>
                <ul class="text-xs text-slate-300 space-y-2 mb-6">
                    <li>&#10003; 10 AM NY Silver Bullet Autotrader</li>
                    <li>&#10003; NQ, ES, GC & CL Execution Engines</li>
                    <li>&#10003; Automated Break-Even & Trailing</li>
                    <li>&#10003; Trade Copier Compatible</li>
                </ul>
            </div>
            <button onclick="checkout('autotrader_suite')" class="w-full bg-white/10 hover:bg-cyan-400 hover:text-black text-white font-bold py-3 rounded-xl transition">Deploy Autotrader ($299)</button>
        </div>

        <div class="card-glow rounded-2xl p-6 flex flex-col justify-between">
            <div>
                <div class="mono text-xs text-amber-300 font-bold">ALL-ACCESS</div>
                <h3 class="text-xl font-bold text-white mt-1">VIP Prop Desk</h3>
                <div class="text-4xl font-black text-amber-300 my-4">$499 <span class="text-xs font-normal text-slate-400">lifetime</span></div>
                <ul class="text-xs text-slate-300 space-y-2 mb-6">
                    <li>&#10003; All {len(BOTS)} Vault Bots Included</li>
                    <li>&#10003; Full Uncompiled C# Source Code</li>
                    <li>&#10003; 1-on-1 Remote Setup Session</li>
                    <li>&#10003; Private Discord/Telegram Desk</li>
                </ul>
            </div>
            <button onclick="checkout('vip_mastermind')" class="w-full bg-amber-400 hover:bg-amber-300 text-black font-black py-3 rounded-xl transition">Join VIP Desk ($499)</button>
        </div>
    </div>
</section>
"""

FOOTER_HTML = f"""
    <footer class="mt-auto border-t border-white/10 bg-[#020305] py-12 px-6 text-xs text-slate-400">
        <div class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
                <div class="text-white font-bold text-base mb-2">THE FUNDED <span class="text-cyan-400">BIBLE</span></div>
                <p class="text-xs text-slate-400 leading-relaxed">The premier terminal for algorithmic futures prop firm traders. Unbiased drawdown rule audits and institutional C# NinjaScript tools.</p>
            </div>
            <div>
                <div class="text-cyan-400 font-bold mono mb-2">CORE TERMINALS</div>
                <ul class="space-y-1.5">
                    <li><a href="/firms.html" class="hover:text-white transition">Prop Firm Comparison Matrix</a></li>
                    <li><a href="/vault.html" class="hover:text-white transition">Algo Vault ({len(BOTS)} Bots)</a></li>
                    <li><a href="/calculator.html" class="hover:text-white transition">Drawdown & Lot Calculator</a></li>
                    <li><a href="/briefings.html" class="hover:text-white transition">SEO Intelligence Directory</a></li>
                </ul>
            </div>
            <div>
                <div class="text-amber-300 font-bold mono mb-2">TOP PROP AUDITS</div>
                <ul class="space-y-1.5">
                    <li><a href="/review-tradeify.html" class="hover:text-white transition">Tradeify Rules & Payouts</a></li>
                    <li><a href="/review-apex-trader-funding.html" class="hover:text-white transition">Apex Trader Funding Review</a></li>
                    <li><a href="/review-topstep.html" class="hover:text-white transition">Topstep EOD Drawdown Guide</a></li>
                    <li><a href="/review-my-funded-futures.html" class="hover:text-white transition">My Funded Futures Audit</a></li>
                </ul>
            </div>
            <div>
                <div class="text-emerald-400 font-bold mono mb-2">INSTANT CHECKOUT</div>
                <ul class="space-y-1.5">
                    <li><button onclick="checkout('flash_bot')" class="hover:text-white text-left transition">$9 Flash FVG Bot</button></li>
                    <li><button onclick="checkout('master_bundle')" class="hover:text-white text-left transition">$19 Master Bundle</button></li>
                    <li><button onclick="checkout('autotrader_suite')" class="hover:text-white text-left transition">$299 Autotrader Suite</button></li>
                    <li><button onclick="checkout('vip_mastermind')" class="hover:text-white text-left transition">$499 VIP Prop Desk</button></li>
                </ul>
            </div>
        </div>
        <div class="max-w-6xl mx-auto pt-6 border-t border-white/5 flex flex-col sm:flex-row justify-between items-center gap-4">
            <div>&copy; 2026 The Funded Bible LLC. All rights reserved. Code: <strong class="text-amber-300">BIBLE80</strong></div>
            <div class="flex gap-4">
                <a href="/sitemap.xml" class="hover:text-cyan-400">Sitemap</a>
                <a href="/robots.txt" class="hover:text-cyan-400">Robots</a>
                <a href="/briefings.html" class="hover:text-cyan-400">Directory</a>
            </div>
        </div>
    </footer>
    <script>
    async function checkout(tier) {{
        try {{
            const res = await fetch('/api/create-checkout-session', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ tier: tier }})
            }});
            const data = await res.json();
            if (data.url) {{ window.location.href = data.url; return; }}
        }} catch(e) {{}}
        window.location.href = '/vault.html?checkout=' + encodeURIComponent(tier);
    }}

    function filterBots(cat) {{
        document.querySelectorAll('.bot-item').forEach(el => {{
            el.style.display = (cat === 'all' || el.dataset.cat === cat) ? 'flex' : 'none';
        }});
    }}
    </script>
</body>
</html>
"""

HERO_SVG = """
<div class="relative w-full overflow-hidden rounded-3xl border border-cyan-500/30 bg-[#04070b] p-8 md:p-16 mb-16 shadow-[0_0_80px_rgba(0,242,254,0.12)]">
    <div class="absolute inset-0 opacity-20" style="background-image: linear-gradient(to right, #00f2fe20 1px, transparent 1px), linear-gradient(to bottom, #00f2fe20 1px, transparent 1px); background-size: 40px 40px;"></div>
    <svg class="absolute -left-24 -top-12 w-[420px] h-[420px] opacity-25 pointer-events-none" viewBox="0 0 200 200" fill="none">
        <circle cx="100" cy="100" r="85" stroke="#00f2fe" stroke-width="1.5"/>
        <ellipse cx="100" cy="100" rx="45" ry="85" stroke="#00f2fe" stroke-width="1"/>
        <ellipse cx="100" cy="100" rx="70" ry="85" stroke="#00ff9d" stroke-width="0.8"/>
        <ellipse cx="100" cy="100" rx="85" ry="35" stroke="#00f2fe" stroke-width="1"/>
        <ellipse cx="100" cy="100" rx="85" ry="65" stroke="#00ff9d" stroke-width="0.8"/>
    </svg>
    <svg class="absolute bottom-0 right-0 w-full md:w-2/3 h-48 opacity-40 pointer-events-none" viewBox="0 0 800 200" fill="none" preserveAspectRatio="none">
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
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-400/30 text-cyan-300 text-xs font-bold tracking-wider uppercase mb-6">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            NINJATRADER 8 AUTOMATED PROP DESK
        </div>
        <h1 class="text-4xl md:text-6xl font-black tracking-tight text-white leading-[1.1] mb-6">
            PASS PROP FIRMS ON AUTOPILOT. <br/>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-emerald-400 to-amber-300">PROTECT YOUR DRAWDOWN.</span>
        </h1>
        <p class="text-slate-300 text-lg md:text-xl max-w-2xl mb-8 leading-relaxed">
            Institutional C# NinjaScript algorithms, Fair Value Gap execution bots, and automated risk locks built for Tradeify, Apex, and Topstep.
        </p>
        <div class="flex flex-wrap gap-4 items-center">
            <button onclick="checkout('flash_bot')" class="bg-gradient-to-r from-cyan-400 to-emerald-400 hover:from-cyan-300 hover:to-emerald-300 text-black font-black px-8 py-4 rounded-xl text-base shadow-[0_0_30px_rgba(0,255,157,0.35)] transition transform hover:-translate-y-0.5">
                Unlock $9 Flash Bot &rarr;
            </button>
            <a href="/vault.html" class="bg-white/5 hover:bg-white/10 border border-white/15 text-white font-bold px-7 py-4 rounded-xl text-base transition">
                View All {len(BOTS)} Algos
            </a>
        </div>
        <div class="mt-8 flex flex-wrap gap-6 text-xs text-slate-400 font-mono">
            <span>&#10003; INSTANT .ZIP DOWNLOAD</span>
            <span>&#10003; CODE: BIBLE80 (MAX DISCOUNT)</span>
            <span>&#10003; ZERO MONTHLY FEES</span>
        </div>
    </div>
</div>
"""

MINI_CHART_SVG = """
<svg class="w-full h-24 bg-[#030609] rounded-lg border border-cyan-500/20 mb-4 p-2" viewBox="0 0 240 70" fill="none">
    <path d="M5 55 L45 42 L85 48 L125 25 L165 32 L205 12 L235 8" stroke="#00f2fe" stroke-width="2"/>
    <rect x="41" y="36" width="8" height="14" fill="#00ff9d"/>
    <rect x="81" y="42" width="8" height="10" fill="#ef4444"/>
    <rect x="121" y="18" width="8" height="18" fill="#00ff9d"/>
    <rect x="161" y="26" width="8" height="11" fill="#ef4444"/>
    <rect x="201" y="6" width="8" height="20" fill="#00ff9d"/>
    <circle cx="205" cy="6" r="3.5" fill="#00ff9d"/>
</svg>
"""

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

generated_urls = []
def write_page(filename, html_content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    url = f"{DOMAIN}/" if filename == "index.html" else f"{DOMAIN}/{filename}"
    generated_urls.append(url)

# Core Schema
site_schema = json.dumps({
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "The Funded Bible",
    "url": DOMAIN,
    "description": "Futures Prop Firm Directory, Drawdown Calculators & NinjaTrader 8 Automated Bots"
})

# 1. index.html
featured_cards_html = "".join([render_bot_card(b) for b in BOTS[:6]])
top_firms_html = "".join([f"""
<a href="/review-{f['slug']}.html" class="card-glow rounded-2xl p-5 flex justify-between items-center">
    <div>
        <div class="text-lg font-bold text-white">{f['name']}</div>
        <div class="text-xs text-slate-400 mt-0.5">{f['drawdown']} &bull; Up to {f['max_alloc']}</div>
    </div>
    <div class="text-right">
        <span class="mono text-xs bg-amber-400/15 text-amber-300 border border-amber-400/30 px-2.5 py-1 rounded font-bold">{f['code']}</span>
        <div class="text-[11px] text-cyan-400 mt-1 font-semibold">Audit &rarr;</div>
    </div>
</a>""" for f in FIRMS[:4]])

index_html = get_head(
    "The Funded Bible | Pass Futures Prop Firms With NinjaTrader 8 Automated Bots",
    "Deploy C# NinjaScript Fair Value Gap bots and automated drawdown protectors built to pass Tradeify, Apex, Topstep, and My Funded Futures.",
    "index.html",
    site_schema
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
                Explore All {len(BOTS)} Automated Bots in the Vault &rarr;
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

# 2. vault.html (All 102 Bots)
all_cards_html = "".join([render_bot_card(b) for b in BOTS])
write_page("vault.html", get_head(f"The Algorithmic Vault ({len(BOTS)} Systems) | The Funded Bible", "Browse 102 C# NinjaScript indicators, FVG snipers, and automated prop firm bots.", "vault.html", site_schema) + f"""
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

# 3. firms.html
all_firms_cards = "".join([f"""
<div class="card-glow rounded-2xl p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
    <div>
        <span class="mono text-xs text-cyan-400">{f['platform']}</span>
        <h2 class="text-2xl font-bold text-white mt-0.5"><a href="/review-{f['slug']}.html" class="hover:text-cyan-400">{f['name']}</a></h2>
        <p class="text-xs text-slate-400 mt-1">Drawdown: <strong class="text-amber-300">{f['drawdown']}</strong> &bull; Max Allocation: <strong class="text-emerald-400">{f['max_alloc']}</strong> &bull; Profit Split: {f['split']}</p>
    </div>
    <div class="flex items-center gap-3">
        <span class="mono text-xs bg-amber-400/15 text-amber-300 border border-amber-400/30 px-3 py-2 rounded-lg font-bold">Code: {f['code']}</span>
        <a href="/review-{f['slug']}.html" class="bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-extrabold px-4 py-2 rounded-lg text-xs">Full Audit &rarr;</a>
    </div>
</div>""" for f in FIRMS])

write_page("firms.html", get_head("Futures Prop Firm Directory & Rules (2026) | The Funded Bible", "Compare EOD vs Trailing drawdowns, max funding allocations, and discount codes.", "firms.html", site_schema) + f"""
<main class="max-w-5xl mx-auto px-6 py-12">
    <h1 class="text-3xl md:text-5xl font-bold text-white mb-3">2026 Futures Prop Firm Rankings</h1>
    <p class="text-slate-400 mb-8">Side-by-side comparison of drawdown models, scaling limits, and payout rules.</p>
    <div class="space-y-4">{all_firms_cards}</div>
</main>{PRICING_SECTION}""" + FOOTER_HTML)

# 4. calculator.html
write_page("calculator.html", get_head("Prop Firm Drawdown & Contract Size Calculator | The Funded Bible", "Calculate exact Micro (MNQ, MES) and Mini (NQ, ES) contract sizing to protect your trailing drawdown.", "calculator.html", site_schema) + """
<main class="max-w-4xl mx-auto px-6 py-12">
    <h1 class="text-3xl md:text-5xl font-bold text-white mb-3">Drawdown Safe-Lot Calculator</h1>
    <p class="text-slate-400 mb-8 text-sm">Calculate your exact contract limit in seconds before entering a trade.</p>
    <div class="card-glow rounded-2xl p-8 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="space-y-4">
            <div><label class="block text-xs mono text-cyan-400 mb-1">REMAINING DRAWDOWN CUSHION ($)</label><input id="dd" type="number" value="2500" class="w-full bg-[#030508] border border-white/15 rounded-xl p-3 text-white mono"></div>
            <div><label class="block text-xs mono text-cyan-400 mb-1">RISK % OF CUSHION PER TRADE</label><input id="riskPct" type="number" value="10" class="w-full bg-[#030508] border border-white/15 rounded-xl p-3 text-white mono"></div>
            <div><label class="block text-xs mono text-cyan-400 mb-1">STOP LOSS DISTANCE (POINTS)</label><input id="pts" type="number" value="15" class="w-full bg-[#030508] border border-white/15 rounded-xl p-3 text-white mono"></div>
            <button onclick="calc()" class="w-full bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-black py-3.5 rounded-xl">Calculate Safe Lot</button>
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

# 5. Programmatic SEO Pages (Reviews, Versus, Product Bots)
directory_links = []

for f in FIRMS:
    slug = f"review-{f['slug']}.html"
    title = f"{f['name']} Review 2026: {f['drawdown']} Rules & Promo Code {f['code']}"
    desc = f"Comprehensive 2026 audit of {f['name']}. Learn how to pass the {f['max_alloc']} evaluation with NinjaTrader 8 bots and claim discount code {f['code']}."
    write_page(slug, get_head(title, desc, slug, site_schema) + f"""
    <main class="max-w-4xl mx-auto px-6 py-12">
        <div class="mb-4"><a href="/firms.html" class="mono text-xs text-cyan-400 hover:underline">&larr; Back to Prop Firm Directory</a></div>
        <h1 class="text-3xl md:text-5xl font-bold text-white mb-4">{f['name']} Review & Passing Guide</h1>
        <p class="text-slate-300 mb-8">{desc}</p>
        <div class="card-glow rounded-2xl p-6 grid grid-cols-2 md:grid-cols-4 gap-4 mono text-xs mb-8">
            <div><span class="text-slate-400 block">MAX ALLOCATION</span><strong class="text-emerald-400 text-base">{f['max_alloc']}</strong></div>
            <div><span class="text-slate-400 block">PROFIT SPLIT</span><strong class="text-white text-base">{f['split']}</strong></div>
            <div><span class="text-slate-400 block">DRAWDOWN</span><strong class="text-cyan-400 text-base">{f['drawdown']}</strong></div>
            <div><span class="text-slate-400 block">DISCOUNT CODE</span><strong class="text-amber-300 text-base">{f['code']}</strong></div>
        </div>
        <h2 class="text-2xl font-bold text-white mb-3">Passing {f['name']} Without Violations</h2>
        <p class="text-slate-300 leading-relaxed mb-6">Traders often struggle with intraday or end-of-day drawdowns when trading volatile NQ minis. Use our $9 Flash Bot and trailing drawdown killswitch to hard-lock risk limits directly inside {f['platform']}.</p>
    </main>{PRICING_SECTION}""" + FOOTER_HTML)
    directory_links.append((slug, title))

for i in range(len(FIRMS)):
    for j in range(i + 1, len(FIRMS)):
        f1, f2 = FIRMS[i], FIRMS[j]
        slug = f"compare-{f1['slug']}-vs-{f2['slug']}.html"
        title = f"{f1['name']} vs {f2['name']} (2026): Which Prop Firm is Best?"
        desc = f"Compare {f1['name']} vs {f2['name']}. Drawdown rules ({f1['drawdown']} vs {f2['drawdown']}), profit splits, and evaluation scaling."
        write_page(slug, get_head(title, desc, slug, site_schema) + f"""
        <main class="max-w-4xl mx-auto px-6 py-12">
            <div class="mb-4"><a href="/firms.html" class="mono text-xs text-cyan-400 hover:underline">&larr; Back to Prop Firm Directory</a></div>
            <h1 class="text-3xl md:text-5xl font-bold text-white mb-4">{f1['name']} vs {f2['name']}</h1>
            <p class="text-slate-300 mb-8">{desc}</p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                <div class="card-glow rounded-2xl p-6">
                    <h2 class="text-2xl font-bold text-cyan-400 mb-3">{f1['name']}</h2>
                    <ul class="text-sm space-y-2 text-slate-300">
                        <li><strong>Max Allocation:</strong> {f1['max_alloc']}</li>
                        <li><strong>Drawdown:</strong> {f1['drawdown']}</li>
                        <li><strong>Split:</strong> {f1['split']}</li>
                        <li><strong>Promo Code:</strong> <span class="mono text-amber-300">{f1['code']}</span></li>
                    </ul>
                </div>
                <div class="card-glow rounded-2xl p-6">
                    <h2 class="text-2xl font-bold text-emerald-400 mb-3">{f2['name']}</h2>
                    <ul class="text-sm space-y-2 text-slate-300">
                        <li><strong>Max Allocation:</strong> {f2['max_alloc']}</li>
                        <li><strong>Drawdown:</strong> {f2['drawdown']}</li>
                        <li><strong>Split:</strong> {f2['split']}</li>
                        <li><strong>Promo Code:</strong> <span class="mono text-amber-300">{f2['code']}</span></li>
                    </ul>
                </div>
            </div>
        </main>{PRICING_SECTION}""" + FOOTER_HTML)
        directory_links.append((slug, title))

for b in BOTS:
    slug = f"bot-{b['slug']}.html"
    title = f"{b['name']} | NinjaTrader 8 Automated Bot ({b['market']})"
    desc = f"{b['desc']} Backtested win rate: {b['win']}. Instant C# NinjaScript .zip download."
    prod_schema = json.dumps({
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": b["name"],
        "description": b["desc"],
        "offers": {"@type": "Offer", "priceCurrency": "USD", "price": b["price"], "availability": "https://schema.org/InStock"}
    })
    write_page(slug, get_head(title, desc, slug, prod_schema) + f"""
    <main class="max-w-4xl mx-auto px-6 py-12">
        <div class="mb-4"><a href="/vault.html" class="mono text-xs text-cyan-400 hover:underline">&larr; Back to Bot Vault</a></div>
        <div class="mono text-xs text-cyan-400 mb-2">{b['market']} // BACKTESTED WIN RATE: {b['win']}</div>
        <h1 class="text-3xl md:text-5xl font-bold text-white mb-4">{b['name']}</h1>
        <p class="text-slate-300 text-lg mb-8">{b['desc']}</p>
        <div class="card-glow rounded-2xl p-8 flex flex-col md:flex-row justify-between items-center gap-6">
            <div>
                <div class="text-xs mono text-slate-400">ONE-TIME DIGITAL LICENSE</div>
                <div class="text-5xl font-black text-white mt-1">${b['price']}</div>
                <div class="text-xs text-emerald-400 mt-2">&#10003; Instant NinjaTrader 8 .zip + ATM Drawdown Guard</div>
            </div>
            <button onclick="checkout('{b['tier']}')" class="bg-gradient-to-r from-cyan-400 to-emerald-400 text-black font-black px-8 py-4 rounded-xl text-base">
                Unlock Now (${b['price']}) &rarr;
            </button>
        </div>
    </main>{PRICING_SECTION}""" + FOOTER_HTML)
    directory_links.append((slug, title))

# 6. briefings.html (Site Directory)
links_list = "".join([f'<li class="py-2 border-b border-white/5"><a href="/{s}" class="text-cyan-400 hover:underline text-sm font-semibold">{t}</a></li>' for s, t in directory_links])
write_page("briefings.html", get_head("Site Directory & SEO Index | The Funded Bible", "Crawlable index of all verified prop firm audits, versus guides, and NinjaScript bots.", "briefings.html", site_schema) + f"""
<main class="max-w-4xl mx-auto px-6 py-12">
    <h1 class="text-3xl font-bold text-white mb-6">Complete Site Directory ({len(generated_urls)+1} Pages)</h1>
    <ul class="card-glow rounded-2xl p-6">{links_list}</ul>
</main>""" + FOOTER_HTML)

# 7. sitemap.xml & robots.txt
sitemap_items = "\n".join([f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>daily</changefreq><priority>0.9</priority></url>" for u in generated_urls])
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap_items}\n</urlset>')
with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")

print(f"[SUCCESS] Rebuilt {len(generated_urls)} fully linked pages, payments handler, and sitemap.xml!")
