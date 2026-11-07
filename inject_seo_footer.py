import os
import re

seo_footer_html = """
<!-- TFB SEO INTERNAL LINK MESH START -->
<footer id="tfb-seo-footer-mesh" style="background:#04060a;border-top:1px solid #1e293b;padding:56px 5% 36px;margin-top:70px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#94a3b8;">
    <div style="max-width:1240px;margin:0 auto;">
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:28px;margin-bottom:40px;">
            <div>
                <div style="color:#10b981;font-weight:900;font-size:1.1rem;letter-spacing:0.8px;margin-bottom:14px;">THE FUNDED BIBLE</div>
                <p style="font-size:0.86rem;line-height:1.6;color:#64748b;margin-bottom:14px;">
                    Institutional automated trading algorithms, NinjaTrader 8 indicators, ATM drawdown defenders, and prop firm execution systems engineered to pass and scale funded accounts.
                </p>
                <a href="/bots-catalog.html" style="display:inline-block;background:rgba(16,185,129,0.12);color:#10b981;border:1px solid #10b981;padding:6px 12px;border-radius:6px;font-size:0.8rem;font-weight:800;text-decoration:none;">
                    Explore All 100 Prop Bots ($9) →
                </a>
            </div>
            <div>
                <h4 style="color:#f1f5f9;font-size:0.88rem;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;">Futures Prop Bots ($9)</h4>
                <ul style="list-style:none;padding:0;margin:0;font-size:0.85rem;line-height:2.0;">
                    <li><a href="/bots/nq-ict-silver-bullet-sniper-bot-001.html" style="color:#94a3b8;text-decoration:none;">NQ ICT Silver Bullet Bot #001</a></li>
                    <li><a href="/bots/nq-ny-open-killzone-scalper-bot-002.html" style="color:#94a3b8;text-decoration:none;">NQ NY Open Killzone Scalper #002</a></li>
                    <li><a href="/bots/es-vwap-institutional-bounce-bot-013.html" style="color:#94a3b8;text-decoration:none;">ES VWAP Institutional Bounce #013</a></li>
                    <li><a href="/bots/gc-orderblock-liquidity-sweep-bot-024.html" style="color:#94a3b8;text-decoration:none;">Gold (GC) Orderblock Sweep #024</a></li>
                    <li><a href="/bots/cl-delta-footprint-absorption-bot-035.html" style="color:#94a3b8;text-decoration:none;">Crude Oil (CL) Delta Footprint #035</a></li>
                    <li><a href="/bots/ym-trailing-drawdown-defender-bot-047.html" style="color:#94a3b8;text-decoration:none;">Mini-Dow (YM) Drawdown Defender #047</a></li>
                </ul>
            </div>
            <div>
                <h4 style="color:#f1f5f9;font-size:0.88rem;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;">Forex, Gold &amp; Crypto Bots</h4>
                <ul style="list-style:none;padding:0;margin:0;font-size:0.85rem;line-height:2.0;">
                    <li><a href="/bots/rty-fair-value-gap-auto-sniper-bot-058.html" style="color:#94a3b8;text-decoration:none;">Russell 2000 (RTY) FVG Sniper #058</a></li>
                    <li><a href="/bots/eurusd-london-breakout-velocity-bot-066.html" style="color:#94a3b8;text-decoration:none;">EUR/USD London Breakout Bot #066</a></li>
                    <li><a href="/bots/gbpusd-ny-open-killzone-scalper-bot-072.html" style="color:#94a3b8;text-decoration:none;">GBP/USD Killzone Scalper Bot #072</a></li>
                    <li><a href="/bots/xauusd-ict-silver-bullet-sniper-bot-081.html" style="color:#94a3b8;text-decoration:none;">XAU/USD Spot Gold Sniper #081</a></li>
                    <li><a href="/bots/btc-cumulative-delta-divergence-bot-099.html" style="color:#94a3b8;text-decoration:none;">Micro Bitcoin (BTC) CVD Bot #099</a></li>
                    <li><a href="/bots/btc-power-hour-momentum-closer-bot-100.html" style="color:#94a3b8;text-decoration:none;">BTC Power Hour Momentum #100</a></li>
                </ul>
            </div>
            <div>
                <h4 style="color:#f1f5f9;font-size:0.88rem;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;">Prop Firm Terminal &amp; Tiers</h4>
                <ul style="list-style:none;padding:0;margin:0;font-size:0.85rem;line-height:2.0;">
                    <li><a href="/index.html" style="color:#94a3b8;text-decoration:none;">Live Institutional Terminal</a></li>
                    <li><a href="/bots-catalog.html" style="color:#10b981;font-weight:700;text-decoration:none;">All 100 Automated Bots ($9 Flash Lock)</a></li>
                    <li><a href="/vault.html?tier=bot9&price=9&promo=BIBLE80" style="color:#f59e0b;font-weight:700;text-decoration:none;">$9 NT8 Bot Instant ZIP Download</a></li>
                    <li><a href="/vault.html" style="color:#94a3b8;text-decoration:none;">$39 Execution Playbook &amp; Equity Simulator</a></li>
                    <li><a href="/firms.html" style="color:#94a3b8;text-decoration:none;">Apex vs Tradeify vs MFFU Comparison</a></li>
                    <li><a href="/calculator.html" style="color:#94a3b8;text-decoration:none;">Trailing Drawdown Risk Calculator</a></li>
                    <li><a href="/sitemap.xml" style="color:#64748b;text-decoration:none;">XML Sitemap (100+ Indexed Pages)</a></li>
                </ul>
            </div>
        </div>
        <div style="border-top:1px solid #111827;padding-top:20px;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;font-size:0.78rem;color:#475569;gap:12px;">
            <div>&copy; 2026 The Funded Bible (thefundedbible.com). All Rights Reserved. Engineered for NinjaTrader 8, TradeLocker &amp; Replikanto.</div>
            <div> High-Speed Indexing Active • Verified $9 Prop Firm Automation</div>
        </div>
    </div>
</footer>
<!-- TFB SEO INTERNAL LINK MESH END -->
"""

patched_count = 0
for root, dirs, files in os.walk("."):
    if ".git" in root or "node_modules" in root:
        continue
    for file in files:
        if file.endswith(".html") and file not in ["admin.html", "404.html"]:
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            orig = content
            # Strip previous SEO footer mesh if re-running
            content = re.sub(
                r'<!-- TFB SEO INTERNAL LINK MESH START -->.*?<!-- TFB SEO INTERNAL LINK MESH END -->',
                '',
                content,
                flags=re.DOTALL
            )

            # Inject cleanly right before </body>
            if "</body>" in content:
                content = content.replace("</body>", seo_footer_html + "\n</body>", 1)
            else:
                content = content + "\n" + seo_footer_html

            if content != orig:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                patched_count += 1

print(f"Successfully injected SEO Internal Link Mesh Footer into {patched_count} HTML pages!")
