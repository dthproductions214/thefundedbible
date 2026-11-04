import os
import datetime

SITE_URL = "https://www.thefundedbible.com"
TODAY = datetime.datetime.utcnow().strftime("%Y-%m-%d")
DISPLAY_DATE = datetime.datetime.utcnow().strftime("%B %d, %Y")

FIRMS = [
    {"slug": "myfundedfutures", "name": "MyFundedFutures (MFFU)", "dd": "End-of-Day (EOD) Static", "act": "$0 ZERO Activation Fee", "max_pa": "5 Active Funded", "split": "90% / 10% Split", "code": "BIBLE80", "url": "https://myfundedfutures.com/?ref=BIBLE80"},
    {"slug": "apex-trader-funding", "name": "Apex Trader Funding", "dd": "Intraday Trailing & EOD Options", "act": "One-Time PA Fee ($140)", "max_pa": "20 Active PAs Allowed", "split": "100% First $25K", "code": "BIBLE80", "url": "https://apextraderfunding.com/?c=BIBLE80"},
    {"slug": "topstep", "name": "Topstep (TopstepX)", "dd": "End-of-Day (EOD) Balance", "act": "$0 No-Fee Path / $149 XFA", "max_pa": "5 Linked XFAs", "split": "90% / 10% Split", "code": "BIBLE", "url": "https://www.topstep.com/"},
    {"slug": "tradeify", "name": "Tradeify Futures", "dd": "End-of-Day (EOD) Trailing Lock", "act": "$0 ZERO Activation Fee", "max_pa": "Multi-Account Scaling", "split": "90% / 10% Split", "code": "BIBLE80", "url": "https://tradeify.co/"},
    {"slug": "take-profit-trader", "name": "Take Profit Trader", "dd": "EOD in Eval / Day-1 Payout", "act": "$130 PRO Fee (Refundable)", "max_pa": "5 PRO Accounts", "split": "80% / 20% (90% PRO+)", "code": "BIBLE80", "url": "https://takeprofittrader.com/"},
    {"slug": "alpha-futures", "name": "Alpha Futures", "dd": "End-of-Day (EOD) Balance", "act": "$0 Zero Activation Option", "max_pa": "$300K Max Allocation", "split": "Up to 90% Split", "code": "BIBLE80", "url": "https://alpha-futures.com/"},
    {"slug": "lucid-trading", "name": "Lucid Trading", "dd": "End-of-Day (EOD) Trailing", "act": "$0 Activation Fee", "max_pa": "5 Funded Accounts", "split": "90% / 10% Split", "code": "BIBLE80", "url": "https://myfundedfutures.com/?ref=BIBLE80"},
    {"slug": "top-one-futures", "name": "Top One Futures", "dd": "Static / EOD Drawdown", "act": "$0 Included", "max_pa": "$300K Active Allocation", "split": "90% Profit Split", "code": "BIBLE80", "url": "https://myfundedfutures.com/?ref=BIBLE80"},
    {"slug": "bulenox", "name": "Bulenox", "dd": "Option 1 Trailing / Option 2 EOD", "act": "One-Time Master Fee", "max_pa": "11 Master Accounts", "split": "100% First $10K", "code": "BIBLE80", "url": "https://bulenox.com/"},
    {"slug": "fundednext-futures", "name": "FundedNext Futures", "dd": "End-of-Day (EOD) Static", "act": "$0 Activation Fee", "max_pa": "$300K Max Allocation", "split": "Up to 90% Split", "code": "BIBLE80", "url": "https://fundednext.com/"},
    {"slug": "tradeday", "name": "TradeDay", "dd": "End-of-Day (EOD) Trailing", "act": "$0 Monthly Funded Fee", "max_pa": "3 Funded Accounts", "split": "Up to 90% Split", "code": "BIBLE", "url": "https://tradeday.com/"},
    {"slug": "blusky-trading", "name": "BluSky Trading", "dd": "End-of-Day (EOD) & Static", "act": "$0 Setup Fee to BluLive", "max_pa": "4 Funded Accounts", "split": "90% / 10% Split", "code": "BIBLE80", "url": "https://blusky.pro/"}
]

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | The Funded Bible™</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{site_url}/{filename}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{
        "@type": "Question",
        "name": "{faq_q1}",
        "acceptedAnswer": {{ "@type": "Answer", "text": "{faq_a1}" }}
      }},
      {{
        "@type": "Question",
        "name": "What is the verified 80% off promo code for futures prop firms?",
        "acceptedAnswer": {{ "@type": "Answer", "text": "Use code BIBLE80 or BIBLE at checkout for up to 80% off evaluations and $0 activation fee promotions." }}
      }}
    ]
  }}
  </script>
  <style>
    :root {{
      --bg-obsidian: #030508; --bg-panel: rgba(11, 15, 25, 0.92);
      --gold: #f59e0b; --gold-bright: #fbbf24; --emerald: #10b981;
      --text-main: #f8fafc; --text-muted: #94a3b8;
      --border-subtle: rgba(255, 255, 255, 0.08); --border-gold: rgba(245, 158, 11, 0.35);
      --font-display: 'Space Grotesk', sans-serif; --font-sans: 'Plus Jakarta Sans', sans-serif; --font-mono: 'JetBrains Mono', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg-obsidian);
      background-image: radial-gradient(circle at 15% 10%, rgba(245, 158, 11, 0.09), transparent 40%),
                        radial-gradient(circle at 85% 25%, rgba(16, 185, 129, 0.07), transparent 40%);
      color: var(--text-main); font-family: var(--font-sans); min-height: 100vh; line-height: 1.6; padding-bottom: 80px;
    }}
    .sticky-command-header {{ position: sticky; top: 0; z-index: 9999; background: #04060a; border-bottom: 1px solid var(--border-gold); }}
    .nav-bar {{ display: flex; justify-content: space-between; align-items: center; max-width: 1240px; margin: 0 auto; padding: 14px 20px; flex-wrap: wrap; gap: 12px; }}
    .brand-logo {{ display: flex; align-items: center; gap: 10px; text-decoration: none; color: #fff; font-family: var(--font-display); font-weight: 800; font-size: 20px; }}
    .brand-badge {{ background: var(--gold); color: #000; font-family: var(--font-mono); font-weight: 800; font-size: 11px; padding: 3px 7px; border-radius: 4px; }}
    .nav-links {{ display: flex; gap: 18px; align-items: center; flex-wrap: wrap; }}
    .nav-links a {{ color: var(--text-muted); text-decoration: none; font-size: 13px; font-weight: 600; }}
    .nav-links a:hover {{ color: var(--gold-bright); }}
    .container {{ max-width: 1140px; margin: 0 auto; padding: 36px 20px; }}
    .panel {{ background: var(--bg-panel); border: 1px solid var(--border-gold); border-radius: 16px; padding: 32px; margin-bottom: 24px; box-shadow: 0 20px 50px rgba(0,0,0,0.85); }}
    .code-pill {{ background: rgba(245, 158, 11, 0.15); border: 1px solid var(--gold); color: #fff; padding: 4px 10px; border-radius: 4px; font-family: var(--font-mono); font-weight: 700; cursor: pointer; }}
    table.cmp-table {{ width: 100%; border-collapse: collapse; font-family: var(--font-mono); font-size: 13px; margin: 22px 0; }}
    table.cmp-table th {{ background: #060911; color: var(--gold-bright); padding: 14px; text-align: left; border-bottom: 1px solid var(--border-gold); }}
    table.cmp-table td {{ padding: 14px; border-bottom: 1px solid var(--border-subtle); color: #fff; }}
    .btn-gold {{ background: linear-gradient(135deg, var(--gold-bright), #d97706); color: #000; font-family: var(--font-mono); font-weight: 800; font-size: 13px; padding: 13px 22px; border-radius: 8px; text-decoration: none; display: inline-block; }}
  </style>
</head>
<body>
  <header class="sticky-command-header">
    <nav class="nav-bar">
      <a href="index.html" class="brand-logo"><span>THE FUNDED BIBLE</span><span class="brand-badge">SEO DESK</span></a>
      <div class="nav-links">
        <a href="index.html">Live Command Desk</a>
        <a href="firms.html">12-Firm Matrix</a>
        <a href="calculator.html">Drawdown Sizer</a>
        <a href="briefings.html">Daily Briefings</a>
        <a href="vault.html">Member Vault</a>
      </div>
    </nav>
  </header>

  <main class="container">
    <div class="panel">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:12px;">
        <span style="font-family:var(--font-mono);font-size:11px;color:var(--emerald);font-weight:700;">● VERIFIED INSTITUTIONAL AUDIT • UPDATED {display_date}</span>
        <span class="code-pill" onclick="navigator.clipboard.writeText('BIBLE80');this.textContent='COPIED BIBLE80 ✓';">COPY 80% OFF CODE: BIBLE80</span>
      </div>
      <h1 style="font-family:var(--font-display);font-size:clamp(26px,3.6vw,42px);font-weight:800;line-height:1.12;margin-bottom:14px;">{h1}</h1>
      <p style="color:var(--text-muted);font-size:15.5px;margin-bottom:20px;">{desc}</p>

      <table class="cmp-table">
        <thead>
          <tr><th>Audit Metric</th><th>{col_a_title}</th><th>{col_b_title}</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Drawdown Model</strong></td><td>{dd_a}</td><td style="color:var(--emerald);font-weight:700;">{dd_b}</td></tr>
          <tr><td><strong>Activation Fee</strong></td><td>{act_a}</td><td style="color:var(--gold-bright);font-weight:700;">{act_b}</td></tr>
          <tr><td><strong>Scaling Capacity</strong></td><td>{max_a}</td><td>{max_b}</td></tr>
          <tr><td><strong>Payout Split</strong></td><td>{split_a}</td><td>{split_b}</td></tr>
          <tr><td><strong>Verified Discount Code</strong></td><td><span class="code-pill">BIBLE80</span></td><td><span class="code-pill">BIBLE80</span></td></tr>
        </tbody>
      </table>

      <div style="background:#060911;border:1px solid var(--border-subtle);border-left:4px solid var(--emerald);padding:18px;border-radius:10px;margin:22px 0;">
        <strong style="font-family:var(--font-mono);color:var(--emerald);font-size:12px;">MECHANICAL SIZING VERDICT:</strong>
        <p style="color:#e2e8f0;font-size:14px;margin-top:6px;">{verdict}</p>
      </div>

      <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px;">
        <a href="/api/create-checkout-session?tier=flash_9" class="btn-gold">GET THE $9 7-DAY PASS BLUEPRINT ⚡</a>
        <a href="/api/create-checkout-session?tier=risk_terminal_39" class="btn-gold" style="background:#111827;color:#fff;border:1px solid var(--gold);">DEPLOY $39 NT8 RISK SUITE →</a>
        <a href="firms.html" class="btn-gold" style="background:transparent;color:var(--gold-bright);border:1px solid var(--border-subtle);">FULL 12-FIRM MATRIX</a>
      </div>
    </div>
  </main>

  <div id="tfb-sticky-bottom-bar" style="position:fixed;bottom:0;left:0;right:0;z-index:9995;background:rgba(4,6,10,0.96);border-top:1px solid rgba(245,158,11,0.4);padding:10px 20px;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;font-family:'JetBrains Mono',monospace;">
    <div style="font-size:12px;color:#fff;">
      <span style="color:#10b981;font-weight:800;">● LIVE DESK OFFER:</span> Pass Your Next $50K Combine in 7 Sessions With Mechanical MNQ Sizing
    </div>
    <div style="display:flex;gap:10px;align-items:center;">
      <a href="/api/create-checkout-session?tier=flash_9" style="background:#111827;color:#fbbf24;border:1px solid #f59e0b;padding:7px 14px;border-radius:6px;font-size:12px;font-weight:800;text-decoration:none;">$9 BLUEPRINT</a>
      <a href="/api/create-checkout-session?tier=risk_terminal_39" style="background:linear-gradient(135deg,#fbbf24,#d97706);color:#000;padding:7px 16px;border-radius:6px;font-size:12px;font-weight:800;text-decoration:none;">$39 RISK SUITE ⚡</a>
    </div>
  </div>
<script src="/tfb-closer-bot.js" defer></script>
</body>
</html>
"""

def build_all_seo_pages():
    generated = []

    # 1. Generate all 132 Head-to-Head Firm Matchups (12 x 11)
    for a in FIRMS:
        for b in FIRMS:
            if a["slug"] == b["slug"]:
                continue
            fname = f"{a['slug']}-vs-{b['slug']}.html"
            title = f"{a['name']} vs {b['name']} ({TODAY[:4]} Prop Firm Audit)"
            h1 = f"{a['name']} vs {b['name']}: Drawdown, Activation Fees & Payout Audit"
            desc = f"Side-by-side institutional audit comparing {a['name']} ({a['dd']}, {a['act']}) against {b['name']} ({b['dd']}, {b['act']}). Use promo code BIBLE80 for 80% off."
            verdict = f"When choosing between {a['name']} and {b['name']}, size your micro contracts strictly to 5.5% of your remaining drawdown buffer (5 MNQ on a $50K combine with a 15-point stop). Use {b['name']} for {b['dd']} protection and {a['name']} to scale up to {a['max_pa']}."
            faq_q1 = f"Which prop firm is better: {a['name']} or {b['name']}?"
            faq_a1 = f"{a['name']} offers {a['dd']} with {a['act']} and {a['max_pa']}, whereas {b['name']} provides {b['dd']} with {b['act']} and {b['max_pa']}."

            html = PAGE_TEMPLATE.format(
                title=title, desc=desc, site_url=SITE_URL, filename=fname,
                faq_q1=faq_q1, faq_a1=faq_a1, display_date=DISPLAY_DATE, h1=h1,
                col_a_title=a["name"], col_b_title=b["name"],
                dd_a=a["dd"], dd_b=b["dd"], act_a=a["act"], act_b=b["act"],
                max_a=a["max_pa"], max_b=b["max_pa"], split_a=a["split"], split_b=b["split"],
                verdict=verdict
            )
            with open(fname, "w", encoding="utf-8") as f:
                f.write(html)
            generated.append(fname)

    # 2. Generate 12 Firm-Specific $50K / $100K Lot-Size & Drawdown Guides
    for f in FIRMS:
        fname = f"{f['slug']}-50k-drawdown-rules-lot-size.html"
        title = f"{f['name']} $50K Drawdown Rules & Safe MNQ Lot Size ({TODAY[:4]})"
        h1 = f"{f['name']} $50K & $100K Combine Playbook: Exact MNQ Sizing & Drawdown Defense"
        desc = f"Complete mechanical rule audit for {f['name']}. Learn how to beat the {f['dd']} rule, claim {f['act']}, and apply promo code {f['code']}."
        verdict = f"On {f['name']}, never exceed 5 MNQ contracts on a $50K account (15-point structural stop = $150 risk per trade). That gives your $2,500 drawdown buffer 16.6 consecutive losses of survival room."
        html = PAGE_TEMPLATE.format(
            title=title, desc=desc, site_url=SITE_URL, filename=fname,
            faq_q1=f"What is the safe lot size for a $50K {f['name']} account?",
            faq_a1=verdict, display_date=DISPLAY_DATE, h1=h1,
            col_a_title="Undisciplined Retail Sizing", col_b_title=f"{f['name']} Mechanical Protocol",
            dd_a="3–5 NQ Minis (Blows in 2 trades)", dd_b="5 MNQ Micros (Survives 16.6 losses)",
            act_a="Pays Full Retail Price", act_b=f"{f['act']} (Code: {f['code']})",
            max_a="1 Over-Leveraged Account", max_b=f["max_pa"],
            split_a="Liquidated Before Payout", split_b=f["split"],
            verdict=verdict
        )
        with open(fname, "w", encoding="utf-8") as fp:
            fp.write(html)
        generated.append(fname)

    # 3. Generate Today's Dated NY Session Orderflow Briefing Page
    daily_fname = f"ny-open-futures-briefing-{TODAY}.html"
    daily_html = PAGE_TEMPLATE.format(
        title=f"NY Open Futures Desk Briefing ({DISPLAY_DATE}) — NQ1! & ES1! Playbook",
        desc=f"Institutional CME Futures Prop Desk Briefing for {DISPLAY_DATE}. NQ1! and ES1! Silver Bullet FVG liquidity zones, safe MNQ lot sizing, and 80% off eval codes.",
        site_url=SITE_URL, filename=daily_fname,
        faq_q1=f"What is the safest NQ lot size for {DISPLAY_DATE}?",
        faq_a1="Trade 5 MNQ contracts with a 15-point stop loss ($150 risk) during the 09:50–10:10 EST Silver Bullet window.",
        display_date=DISPLAY_DATE,
        h1=f"NY Session Institutional Futures Briefing — {DISPLAY_DATE}",
        col_a_title="09:30 EST Judas Swing Trap", col_b_title="09:50–10:10 EST Silver Bullet Window",
        dd_a="Whipsaws Asia/London Highs & Lows", dd_b="Clean 5m FVG Reclaim Aligned With VWAP",
        act_a="High Slippage on Market Orders", act_b="Limit Pullback Into 5m Displacement",
        max_a="Avoid Over-Sizing First 15 Mins", max_b="5 MNQ Per $50K Linked Account",
        split_a="Hard 2-Loss (-$300) Lockout", split_b="+30pt ($300) Base-Hit Target",
        verdict=f"Desk Protocol for {DISPLAY_DATE}: Let the 09:30 EST cash open clear overnight liquidity pools first. Execute only on a confirmed 5-minute Fair Value Gap reclaim with 5 MNQ."
    )
    with open(daily_fname, "w", encoding="utf-8") as fp:
        fp.write(daily_html)
    generated.append(daily_fname)

    # 4. Rebuild sitemap.xml with every HTML file in the repository
    all_html = sorted([f for f in os.listdir(".") if f.endswith(".html") and not f.startswith("google")])
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap_lines.append(f"  <url><loc>{SITE_URL}/</loc><lastmod>{TODAY}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>")
    for f in all_html:
        if f in ["index.html", "admin.html", "viral.html"]:
            continue
        prio = "0.9" if f in ["firms.html", "calculator.html", "briefings.html", "vault.html"] else "0.8"
        sitemap_lines.append(f"  <url><loc>{SITE_URL}/{f}</loc><lastmod>{TODAY}</lastmod><changefreq>daily</changefreq><priority>{prio}</priority></url>")
    sitemap_lines.append("</urlset>")
    with open("sitemap.xml", "w", encoding="utf-8") as fp:
        fp.write("\n".join(sitemap_lines))

    print(f"[✓] Generated/Updated {len(generated)} programmatic SEO pages and indexed {len(all_html)} total URLs in sitemap.xml")

if __name__ == "__main__":
    build_all_seo_pages()