import os
import re

master_hero_html = """
<!-- TFB $19 MASTER BUNDLE HERO SHOWCASE START -->
<section id="tfb-master-19-hero" style="max-width:1240px;margin:28px auto;padding:0 20px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    <div style="background:linear-gradient(135deg,#171307 0%,#0b111c 55%,#061a14 100%);border:2px solid #f59e0b;border-radius:16px;padding:28px 32px;box-shadow:0 16px 45px rgba(245,158,11,0.18);display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:24px;position:relative;overflow:hidden;">
        <div style="flex:1;min-width:300px;">
            <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(245,158,11,0.16);border:1px solid #f59e0b;color:#fbbf24;font-size:0.76rem;font-weight:900;padding:4px 12px;border-radius:999px;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:12px;">
                🔥 VIP INSTITUTIONAL VAULT DEAL • SAVE 98% TODAY
            </div>
            <h2 style="color:#ffffff;font-size:1.95rem;line-height:1.2;margin:0 0 10px 0;font-weight:900;">
                Why Buy 1 Bot for $9? Unlock <span style="color:#fbbf24;text-decoration:underline;">ALL 100 Prop Firm Trading Bots</span> for Just <span style="color:#10b981;">$19.00</span>
            </h2>
            <p style="color:#cbd5e1;font-size:0.98rem;line-height:1.55;margin:0 0 14px 0;">
                Get instant 1-click access to the complete <strong>TFB-All-100-Bots-Master-Bundle.zip</strong> archive: all 100 compiled NinjaTrader 8 (.cs) algorithms covering <strong>NQ, ES, Gold (GC), Crude Oil (CL), Mini-Dow (YM), Russell (RTY), EUR/USD, GBP/USD, XAU/USD &amp; Bitcoin</strong>—plus all 10 Auto-Breakeven ATM Drawdown Defenders.
            </p>
            <div style="display:flex;flex-wrap:wrap;gap:16px;font-size:0.82rem;color:#94a3b8;font-weight:600;">
                <span style="color:#34d399;">✔ 100 NinjaScript (.cs) Strategies</span>
                <span style="color:#34d399;">✔ 10 Market ATM XML Templates</span>
                <span style="color:#34d399;">✔ Replikanto 20-Account Playbook</span>
                <span style="color:#fbbf24;">✔ Instant .ZIP Download</span>
            </div>
        </div>
        <div style="background:rgba(5,8,14,0.85);border:1px solid #334155;border-radius:12px;padding:22px 24px;text-align:center;min-width:270px;flex-shrink:0;">
            <div style="font-size:0.78rem;color:#94a3b8;text-transform:uppercase;font-weight:800;letter-spacing:0.5px;">Complete 100-Bot Master Pack</div>
            <div style="margin:8px 0 14px 0;">
                <span style="font-size:2.7rem;font-weight:900;color:#fbbf24;line-height:1;">$19</span>
                <span style="font-size:1.15rem;color:#64748b;text-decoration:line-through;margin-left:6px;">$900</span>
                <span style="display:block;font-size:0.76rem;color:#10b981;font-weight:800;margin-top:4px;">Just $0.19 Per Automated Bot!</span>
            </div>
            <a href="/vault.html?tier=master19&price=19&bump=1&promo=BIBLE80" style="display:block;width:100%;background:linear-gradient(135deg,#f59e0b,#d97706);color:#000000;font-weight:900;font-size:1.02rem;padding:14px 20px;border-radius:8px;text-decoration:none;box-shadow:0 8px 25px rgba(245,158,11,0.35);margin-bottom:8px;">
                UNLOCK ALL 100 BOTS ($19) →
            </a>
            <a href="/bots-catalog.html" style="color:#94a3b8;font-size:0.78rem;text-decoration:underline;">
                Or browse individual $9 bots below
            </a>
        </div>
    </div>
</section>
<!-- TFB $19 MASTER BUNDLE HERO SHOWCASE END -->
"""

target_files = ["bots-catalog.html", "index.html", "firms.html", "calculator.html"]
patched = 0

for fname in target_files:
    if os.path.exists(fname):
        with open(fname, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        orig = content
        # Remove existing hero block if re-running
        content = re.sub(
            r'<!-- TFB \$19 MASTER BUNDLE HERO SHOWCASE START -->.*?<!-- TFB \$19 MASTER BUNDLE HERO SHOWCASE END -->',
            '',
            content,
            flags=re.DOTALL
        )

        # Inject right after </nav> so it sits prominently above the grid/content
        if "</nav>" in content:
            content = content.replace("</nav>", "</nav>\n" + master_hero_html, 1)
        elif "<!-- TFB STICKY $9 FLASH LOCK BANNER END -->" in content:
            content = content.replace(
                "<!-- TFB STICKY $9 FLASH LOCK BANNER END -->",
                "<!-- TFB STICKY $9 FLASH LOCK BANNER END -->\n" + master_hero_html,
                1
            )
        else:
            content = master_hero_html + "\n" + content

        if content != orig:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(content)
            patched += 1
            print(f"Injected $19 Master Bundle Hero Showcase into: {fname}")

print(f"Total core pages updated with $19 Master Bundle Hero: {patched}")
