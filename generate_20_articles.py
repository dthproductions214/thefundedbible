import os
import json
from datetime import datetime

DOMAIN = "https://thefundedbible.com"
ARTICLES_DIR = "articles"
os.makedirs(ARTICLES_DIR, exist_ok=True)
today = datetime.now().strftime("%Y-%m-%d")

# 20 High-Intent Prop Firm Comparison & Bot Execution Topics
TOPICS = [
    ("tradeify-vs-apex-trader-funding-2026", "Tradeify vs Apex Trader Funding (2026): Rules, Drawdown & Payout Speed Compared", "Tradeify", "Apex Trader Funding", "nq-ict-silver-bullet-sniper-bot-001", "NQ ICT Silver Bullet Bot #001"),
    ("myfundedfutures-vs-topstep-2026", "MyFundedFutures vs Topstep (2026): EOD Drawdown & Activation Fees Breakdown", "MyFundedFutures", "Topstep", "es-vwap-institutional-bounce-bot-013", "ES VWAP Institutional Bounce Bot #013"),
    ("take-profit-trader-vs-tradeify-instant-funding", "Take Profit Trader vs Tradeify: Best Prop Firm for Day-1 Payouts in 2026", "Take Profit Trader", "Tradeify", "nq-ny-open-killzone-scalper-bot-002", "NQ NY Open Killzone Scalper #002"),
    ("best-ninjatrader-8-automated-bots-for-apex", "Best NinjaTrader 8 Automated Bots to Pass Apex 50k & 150k Evaluations Fast", "Apex Trader Funding", "Tradeify", "ym-trailing-drawdown-defender-bot-047", "Mini-Dow (YM) Drawdown Defender #047"),
    ("how-to-beat-intraday-trailing-drawdown-prop-firms", "How to Beat Intraday Trailing Drawdown on Prop Firm Accounts Using NT8 Automation", "Apex Trader Funding", "Bulenox", "nq-trailing-drawdown-defender-bot-007", "NQ Trailing Drawdown Defender #007"),
    ("replikanto-copy-trading-20-prop-accounts-setup", "How to Copy Trade 20 Prop Firm Accounts Simultaneously with Replikanto & NinjaTrader 8", "Apex Trader Funding", "Tradeify", "es-ny-open-killzone-scalper-bot-012", "ES NY Open Killzone Scalper #012"),
    ("top-5-no-evaluation-instant-funded-futures-firms", "Top 5 Instant Funded Futures Prop Firms in 2026 (Skip the Evaluation Phase)", "Tradeify", "MyFundedFutures", "gc-orderblock-liquidity-sweep-bot-024", "Gold (GC) Orderblock Sweep Bot #024"),
    ("gold-futures-gc-mgc-prop-firm-scalping-strategy", "Gold Futures (GC & MGC) Prop Firm Scalping Strategy: Passing 50k Evals in 3 Days", "Topstep", "MyFundedFutures", "gc-ict-silver-bullet-sniper-bot-021", "Gold (GC) ICT Silver Bullet Bot #021"),
    ("crude-oil-cl-orderflow-footprint-prop-trading", "Crude Oil (CL) Delta Footprint Absorption: Automated NYMEX Prop Firm Execution", "Take Profit Trader", "Topstep", "cl-delta-footprint-absorption-bot-035", "Crude Oil (CL) Delta Footprint Bot #035"),
    ("alpha-futures-vs-myfundedfutures-payout-rules", "Alpha Futures vs MyFundedFutures: Consistency Rules & Payout Caps Compared", "Alpha Futures", "MyFundedFutures", "nq-fair-value-gap-auto-sniper-bot-008", "NQ Fair Value Gap Auto-Sniper #008"),
    ("bulenox-vs-apex-trader-funding-option-1-vs-eod", "Bulenox EOD vs Apex Trailing Drawdown: Which Prop Firm Fits Automated Bots Best?", "Bulenox", "Apex Trader Funding", "rty-fair-value-gap-auto-sniper-bot-058", "Russell 2000 (RTY) FVG Sniper #058"),
    ("tradelocker-vs-ninjatrader-8-prop-firm-execution", "TradeLocker vs NinjaTrader 8: Latency, Slippage & Bot Automation Comparison", "FundedNext", "Tradeify", "eurusd-london-breakout-velocity-bot-066", "EUR/USD London Breakout Bot #066"),
    ("ict-silver-bullet-10am-ny-session-automated-bot", "Automating the ICT 10:00 AM Silver Bullet Setup on NQ & ES Futures for Prop Firms", "Tradeify", "Topstep", "nq-ict-silver-bullet-sniper-bot-001", "NQ ICT Silver Bullet Bot #001"),
    ("fundednext-futures-vs-topstep-50k-account-review", "FundedNext vs Topstep 50k Account Review: Profit Split, Scaling & Bot Rules", "FundedNext", "Topstep", "gbpusd-ny-open-killzone-scalper-bot-072", "GBP/USD Killzone Scalper Bot #072"),
    ("tradeday-vs-blusky-futures-prop-firm-comparison", "TradeDay vs BluSky Trading: Real Brokerage Transition & Automated Bot Policies", "TradeDay", "BluSky", "es-cumulative-delta-divergence-bot-019", "ES Cumulative Delta Bot #019"),
    ("xauusd-spot-gold-prop-firm-bot-vs-comex-gc", "Trading XAU/USD Spot Gold vs COMEX GC Futures on Funded Accounts: Full Breakdown", "FundedNext", "MyFundedFutures", "xauusd-ict-silver-bullet-sniper-bot-081", "XAU/USD Spot Gold Sniper #081"),
    ("lucid-trading-vs-top-one-futures-prop-comparison", "Lucid Trading vs Top One Futures: Hidden Rules, Drawdown Locks & Payout Proofs", "Lucid Trading", "Top One Futures", "nq-orderblock-liquidity-sweep-bot-004", "NQ Orderblock Sweep Bot #004"),
    ("micro-bitcoin-futures-mbt-prop-firm-bot-strategy", "How to Trade Micro Bitcoin Futures (MBT) on Prop Firm Accounts Using CVD Automation", "MyFundedFutures", "Tradeify", "btc-cumulative-delta-divergence-bot-099", "Micro Bitcoin (BTC) CVD Bot #099"),
    ("prop-firm-consistency-rule-calculator-30-percent-hack", "How to Never Fail the 30% & 40% Prop Firm Consistency Rule: Automated Lot Scaling", "Tradeify", "Take Profit Trader", "es-trailing-drawdown-defender-bot-017", "ES Trailing Drawdown Defender #017"),
    ("pass-50k-prop-firm-evaluation-under-7-days-blueprint", "The 7-Day $50k Prop Firm Evaluation Blueprint: Combining ATM Presets & $9 NT8 Bots", "Apex Trader Funding", "MyFundedFutures", "nq-power-hour-momentum-closer-bot-010", "NQ Power Hour Momentum Bot #010")
]

article_cards = []

for idx, (slug, title, firm_a, firm_b, bot_slug, bot_name) in enumerate(TOPICS, 1):
    filename = f"{slug}.html"
    filepath = os.path.join(ARTICLES_DIR, filename)
    bot_url = f"/bots/{bot_slug}.html"
    checkout_url = f"/vault.html?tier=bot9&price=9&promo=BIBLE80&bot={bot_slug}"

    schema_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": title,
                "datePublished": today,
                "dateModified": today,
                "author": {"@type": "Organization", "name": "The Funded Bible Institutional Desk"},
                "publisher": {"@type": "Organization", "name": "The Funded Bible", "url": DOMAIN},
                "mainEntityOfPage": f"{DOMAIN}/{ARTICLES_DIR}/{filename}"
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f"Does {firm_a} or {firm_b} allow NinjaTrader 8 automated bots?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f"Both {firm_a} and {firm_b} support NinjaTrader 8 execution. Using non-HFT rule-compliant strategies like the {bot_name} with hard daily loss circuit breakers keeps your account within evaluation and funded PA guidelines."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": f"How do I protect my trailing drawdown on {firm_a} and {firm_b}?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Deploy an ATM auto-breakeven trigger at +20 ticks and cap your daily loss at 25% of your total drawdown buffer so a single session never compromises your funded account."
                        }
                    }
                ]
            }
        ]
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | The Funded Bible</title>
    <meta name="description" content="{title}. Compare {firm_a} vs {firm_b} drawdown rules, payout speeds, and unlock the {bot_name} for just $9.">
    <link rel="canonical" href="{DOMAIN}/{ARTICLES_DIR}/{filename}">
    <script type="application/ld+json">{json.dumps(schema_data)}</script>
    <style>
        :root {{ --bg: #07090e; --card: #0f141d; --accent: #10b981; --gold: #f59e0b; --text: #f1f5f9; --muted: #94a3b8; --border: #1e293b; }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.7; }}
        .nav {{ display: flex; justify-content: space-between; align-items: center; padding: 18px 5%; border-bottom: 1px solid var(--border); background: #05070b; }}
        .nav a {{ color: var(--text); text-decoration: none; font-weight: 700; margin-left: 20px; font-size: 0.95rem; }}
        .wrap {{ max-width: 920px; margin: 40px auto; padding: 0 20px; }}
        .kicker {{ display: inline-block; background: rgba(16,185,129,0.12); color: var(--accent); border: 1px solid var(--accent); padding: 4px 12px; border-radius: 999px; font-size: 0.78rem; font-weight: 800; margin-bottom: 14px; }}
        h1 {{ font-size: 2.2rem; line-height: 1.25; margin-bottom: 16px; }}
        h2 {{ font-size: 1.5rem; color: var(--accent); margin: 34px 0 12px; }}
        p {{ color: #cbd5e1; margin-bottom: 16px; font-size: 1.04rem; }}
        table {{ width: 100%; border-collapse: collapse; margin: 24px 0; background: var(--card); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }}
        th, td {{ padding: 14px 16px; text-align: left; border-bottom: 1px solid var(--border); }}
        th {{ background: #05070b; color: var(--accent); font-size: 0.85rem; text-transform: uppercase; }}
        .bot-cta-box {{ background: linear-gradient(145deg, #0d1922, #090d14); border: 2px solid var(--accent); border-radius: 14px; padding: 26px; margin: 32px 0; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 20px; }}
        .btn-green {{ display: inline-block; background: linear-gradient(135deg, #10b981, #059669); color: #000; font-weight: 900; padding: 14px 24px; border-radius: 8px; text-decoration: none; font-size: 1.05rem; }}
        .faq-item {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 18px 20px; margin-bottom: 14px; }}
        .faq-item h3 {{ font-size: 1.1rem; color: #fff; margin-bottom: 6px; }}
    </style>
</head>
<body>
    <nav class="nav">
        <a href="/index.html" style="color:var(--accent);font-size:1.25rem;margin-left:0;">THE FUNDED BIBLE</a>
        <div>
            <a href="/bots-catalog.html" style="color:var(--accent);">100 Bots ($9)</a>
            <a href="/articles/index.html">Intel Briefings</a>
            <a href="/firms.html">Prop Firms</a>
            <a href="/vault.html">The Vault</a>
        </div>
    </nav>
    <div class="wrap">
        <span class="kicker">2026 INSTITUTIONAL PROP DESK BRIEFING #{idx:02d}</span>
        <h1>{title}</h1>
        <p>Choosing between <strong>{firm_a}</strong> and <strong>{firm_b}</strong> in 2026 comes down to three mechanical variables: how the trailing drawdown is calculated (Intraday High-Water Mark vs End-of-Day), how fast payouts clear once you hit the buffer zone, and how efficiently your NinjaTrader 8 automated execution handles opening-bell volatility.</p>

        <div class="bot-cta-box">
            <div style="flex:1;min-width:260px;">
                <div style="color:var(--gold);font-size:0.8rem;font-weight:800;margin-bottom:4px;">RECOMMENDED BOT FOR {firm_a.upper()} &amp; {firm_b.upper()}</div>
                <h3 style="font-size:1.35rem;color:#fff;margin-bottom:6px;">{bot_name} — Instant $9 Flash Lock</h3>
                <p style="margin:0;font-size:0.92rem;color:var(--muted);">Pre-configured NinjaScript (.cs) + ATM Auto-Breakeven XML built to pass 50k &amp; 150k evaluations without breaching daily drawdown.</p>
            </div>
            <div style="display:flex;flex-direction:column;gap:8px;">
                <a href="{checkout_url}" class="btn-green">Unlock Bot for $9.00 →</a>
                <a href="{bot_url}" style="color:var(--accent);font-size:0.85rem;text-align:center;text-decoration:none;font-weight:700;">View Full Backtest Specs →</a>
            </div>
        </div>

        <h2>1. {firm_a} vs {firm_b}: Head-to-Head Execution Matrix</h2>
        <p>Retail traders blow 88% of evaluations because they trade identical contract sizes across different drawdown structures. Here is how {firm_a} and {firm_b} stack up side-by-side right now:</p>
        <table>
            <thead>
                <tr>
                    <th>Rule / Metric</th>
                    <th>{firm_a}</th>
                    <th>{firm_b}</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>50k Max Drawdown</strong></td>
                    <td>$2,000 - $2,500 (Rule-Dependent)</td>
                    <td>$2,000 - $2,500 Trailing / EOD</td>
                </tr>
                <tr>
                    <td><strong>Automated NT8 Bots</strong></td>
                    <td>Supported (Non-HFT / Real Orderflow)</td>
                    <td>Supported with ATM Risk Brackets</td>
                </tr>
                <tr>
                    <td><strong>Recommended Sizing</strong></td>
                    <td>2–3 Micros (MNQ / MES / MGC)</td>
                    <td>2–4 Micros + Auto-Breakeven at +20t</td>
                </tr>
                <tr>
                    <td><strong>Best Matched Algorithm</strong></td>
                    <td><a href="{bot_url}" style="color:var(--accent);font-weight:700;">{bot_name} ($9)</a></td>
                    <td><a href="/bots-catalog.html" style="color:var(--gold);font-weight:700;">View All 100 Bots ($9)</a></td>
                </tr>
            </tbody>
        </table>

        <h2>2. Why Automated ATM Brackets Beat Manual Clicking</h2>
        <p>When NQ or Gold spikes at 9:30 AM or 10:00 AM EST, manual traders hesitate on stops and let a -15 tick pullback turn into a -$1,200 account breach. By running the <a href="{bot_url}" style="color:var(--accent);font-weight:700;">{bot_name}</a> inside NinjaTrader 8, your hard stop, profit target, and +20 tick auto-breakeven trigger fire on the server millisecond.</p>

        <h2>3. Frequently Asked Questions</h2>
        <div class="faq-item">
            <h3>Does {firm_a} or {firm_b} allow NinjaTrader 8 automated bots?</h3>
            <p style="margin:0;font-size:0.95rem;">Yes. Both {firm_a} and {firm_b} support NinjaTrader 8 execution. Running disciplined, non-HFT strategies like the {bot_name} with a hard daily loss circuit breaker keeps your execution clean and compliant.</p>
        </div>
        <div class="faq-item">
            <h3>Where can I download the NinjaScript (.cs) and ATM preset files?</h3>
            <p style="margin:0;font-size:0.95rem;">You can unlock the complete <a href="{checkout_url}" style="color:var(--accent);font-weight:700;">{bot_name} (.ZIP Bundle) for $9 right here</a> or browse all <a href="/bots-catalog.html" style="color:var(--accent);font-weight:700;">100 Prop Firm Trading Bots in the catalog</a>.</p>
        </div>
    </div>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    article_cards.append(f"""
    <div style="background:#0f141d;border:1px solid #1e293b;border-radius:12px;padding:22px;display:flex;flex-direction:column;justify-content:space-between;">
        <div>
            <span style="font-size:0.75rem;color:#10b981;font-weight:800;">BRIEFING #{idx:02d} • {firm_a.upper()} VS {firm_b.upper()}</span>
            <h3 style="font-size:1.18rem;margin:8px 0 10px;"><a href="/{ARTICLES_DIR}/{filename}" style="color:#fff;text-decoration:none;">{title}</a></h3>
            <p style="color:#94a3b8;font-size:0.9rem;margin-bottom:16px;">Full rule comparison, drawdown math, and direct $9 setup for the {bot_name}.</p>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;border-top:1px solid #1e293b;padding-top:12px;">
            <a href="/{ARTICLES_DIR}/{filename}" style="color:#10b981;font-weight:800;font-size:0.88rem;text-decoration:none;">Read Briefing →</a>
            <a href="{bot_url}" style="background:#10b981;color:#000;font-weight:800;font-size:0.8rem;padding:6px 12px;border-radius:6px;text-decoration:none;">Get Bot ($9)</a>
        </div>
    </div>""")

# Build /articles/index.html Hub Page
hub_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prop Firm Comparison Briefings & Automated Bot Playbooks | The Funded Bible</title>
    <meta name="description" content="20+ institutional prop firm comparisons: Tradeify vs Apex, MyFundedFutures vs Topstep, Replikanto copy trading, and $9 NinjaTrader 8 automated bots.">
    <link rel="canonical" href="{DOMAIN}/{ARTICLES_DIR}/index.html">
</head>
<body style="background:#07090e;color:#f1f5f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;margin:0;">
    <nav style="display:flex;justify-content:space-between;align-items:center;padding:18px 5%;border-bottom:1px solid #1e293b;background:#05070b;">
        <a href="/index.html" style="color:#10b981;font-size:1.25rem;font-weight:900;text-decoration:none;">THE FUNDED BIBLE</a>
        <div>
            <a href="/bots-catalog.html" style="color:#10b981;text-decoration:none;font-weight:800;margin-left:20px;">100 Bots ($9)</a>
            <a href="/firms.html" style="color:#f1f5f9;text-decoration:none;font-weight:700;margin-left:20px;">Prop Firms</a>
            <a href="/vault.html" style="color:#f1f5f9;text-decoration:none;font-weight:700;margin-left:20px;">The Vault</a>
        </div>
    </nav>
    <div style="text-align:center;padding:48px 20px 24px;max-width:860px;margin:0 auto;">
        <h1 style="font-size:2.4rem;margin-bottom:10px;">Prop Firm Intelligence &amp; Bot Playbooks</h1>
        <p style="color:#94a3b8;font-size:1.05rem;">Side-by-side drawdown comparisons, payout rules, and automated $9 NinjaTrader 8 execution setups.</p>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px;max-width:1240px;margin:20px auto 60px;padding:0 20px;">
        {"".join(article_cards)}
    </div>
</body>
</html>"""

with open(os.path.join(ARTICLES_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(hub_html)

print(f"Generated {len(TOPICS)} SEO comparison articles + /articles/index.html hub!")

# Rebuild sitemap.xml with all pages, 100 bots, and 20 articles
urls = []
for root, dirs, files in os.walk("."):
    if ".git" in root or "node_modules" in root:
        continue
    for file in files:
        if file.endswith(".html") and file not in ["admin.html", "404.html"]:
            rel = os.path.relpath(os.path.join(root, file), ".").replace("\\", "/")
            url = f"{DOMAIN}/" if rel == "index.html" else f"{DOMAIN}/{rel}"
            prio = "1.0" if rel in ["index.html", "bots-catalog.html", "articles/index.html"] else "0.85"
            urls.append((url, today, prio))

sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url, lastmod, prio in sorted(urls):
    sitemap_xml += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <priority>{prio}</priority>\n  </url>\n"
sitemap_xml += "</urlset>"

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print(f"Updated sitemap.xml with {len(urls)} total indexed URLs!")
