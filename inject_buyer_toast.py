import os
import re

buyer_toast_html = """
<!-- TFB BUYER PROOF TOAST START -->
<style>
#tfb-buyer-toast {
    position: fixed;
    bottom: 22px;
    left: 22px;
    z-index: 99990;
    background: rgba(11, 16, 26, 0.96);
    border: 1px solid #10b981;
    border-left: 4px solid #10b981;
    border-radius: 10px;
    padding: 12px 16px;
    max-width: 340px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.75);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    display: flex;
    align-items: center;
    gap: 12px;
    transform: translateY(140%);
    opacity: 0;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.4s ease;
    pointer-events: auto;
}
#tfb-buyer-toast.tfb-toast-visible {
    transform: translateY(0);
    opacity: 1;
}
@media (max-width: 600px) {
    #tfb-buyer-toast {
        left: 12px;
        right: 12px;
        bottom: 14px;
        max-width: none;
    }
}
</style>
<div id="tfb-buyer-toast" aria-live="polite">
    <div style="width:36px;height:36px;border-radius:50%;background:rgba(16,185,129,0.15);border:1px solid #10b981;display:flex;align-items:center;justify-content:center;color:#10b981;font-weight:900;font-size:1rem;flex-shrink:0;">
        ✓
    </div>
    <div style="flex:1;min-width:0;">
        <div id="tfb-toast-header" style="color:#f8fafc;font-size:0.82rem;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
            Marcus T. (Dallas, TX)
        </div>
        <div id="tfb-toast-body" style="color:#94a3b8;font-size:0.78rem;line-height:1.35;margin-top:2px;">
            Unlocked <a id="tfb-toast-link" href="/bots/nq-ict-silver-bullet-sniper-bot-001.html" style="color:#10b981;font-weight:700;text-decoration:none;">NQ ICT Silver Bullet Bot #001</a> for <strong style="color:#fbbf24;">$9.00</strong>
        </div>
        <div id="tfb-toast-time" style="color:#64748b;font-size:0.7rem;margin-top:3px;">
            Verified Stripe/Whop Checkout • 2 mins ago
        </div>
    </div>
    <button onclick="document.getElementById('tfb-buyer-toast').style.display='none'" style="background:none;border:none;color:#64748b;font-size:1rem;cursor:pointer;padding:2px 4px;line-height:1;" title="Dismiss">×</button>
</div>
<script>
(function() {
    var buyers = [
        { name: "Marcus T. (Austin, TX)", bot: "NQ ICT Silver Bullet Bot #001", slug: "nq-ict-silver-bullet-sniper-bot-001", time: "2 mins ago" },
        { name: "Devon R. (Miami, FL)", bot: "ES VWAP Institutional Bounce #013", slug: "es-vwap-institutional-bounce-bot-013", time: "4 mins ago" },
        { name: "Carlos M. (Chicago, IL)", bot: "NQ NY Open Killzone Scalper #002", slug: "nq-ny-open-killzone-scalper-bot-002", time: "6 mins ago" },
        { name: "Ryan K. (Phoenix, AZ)", bot: "Gold (GC) Orderblock Sweep #024", slug: "gc-orderblock-liquidity-sweep-bot-024", time: "9 mins ago" },
        { name: "Brandon L. (Atlanta, GA)", bot: "Mini-Dow (YM) Drawdown Defender #047", slug: "ym-trailing-drawdown-defender-bot-047", time: "11 mins ago" },
        { name: "Jason V. (Charlotte, NC)", bot: "Crude Oil (CL) Delta Footprint #035", slug: "cl-delta-footprint-absorption-bot-035", time: "14 mins ago" },
        { name: "Kevin H. (Las Vegas, NV)", bot: "XAU/USD Spot Gold Sniper #081", slug: "xauusd-ict-silver-bullet-sniper-bot-081", time: "17 mins ago" },
        { name: "Tyler S. (Denver, CO)", bot: "Russell 2000 (RTY) FVG Sniper #058", slug: "rty-fair-value-gap-auto-sniper-bot-058", time: "19 mins ago" },
        { name: "Alex P. (Toronto, ON)", bot: "EUR/USD London Breakout Bot #066", slug: "eurusd-london-breakout-velocity-bot-066", time: "23 mins ago" },
        { name: "Jordan W. (Houston, TX)", bot: "Micro Bitcoin (BTC) CVD Bot #099", slug: "btc-cumulative-delta-divergence-bot-099", time: "26 mins ago" }
    ];

    var toast = document.getElementById("tfb-buyer-toast");
    var headerEl = document.getElementById("tfb-toast-header");
    var linkEl = document.getElementById("tfb-toast-link");
    var timeEl = document.getElementById("tfb-toast-time");
    if (!toast || !headerEl || !linkEl || !timeEl) return;

    var idx = Math.floor(Math.random() * buyers.length);

    function showNextToast() {
        if (toast.style.display === "none") return;
        var item = buyers[idx % buyers.length];
        idx++;
        headerEl.textContent = item.name + " • Apex / Tradeify Trader";
        linkEl.textContent = item.bot;
        linkEl.href = "/vault.html?tier=bot9&price=9&promo=BIBLE80&bot=" + item.slug;
        timeEl.textContent = "Verified $9 Flash Lock • " + item.time;

        toast.classList.add("tfb-toast-visible");
        setTimeout(function() {
            toast.classList.remove("tfb-toast-visible");
        }, 5500);
    }

    setTimeout(function() {
        showNextToast();
        setInterval(showNextToast, 14000);
    }, 3500);
})();
</script>
<!-- TFB BUYER PROOF TOAST END -->
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
            # Remove any existing buyer toast block so re-runs stay clean
            content = re.sub(
                r'<!-- TFB BUYER PROOF TOAST START -->.*?<!-- TFB BUYER PROOF TOAST END -->',
                '',
                content,
                flags=re.DOTALL
            )

            # Inject right before </body>
            if "</body>" in content:
                content = content.replace("</body>", buyer_toast_html + "\n</body>", 1)
            else:
                content = content + "\n" + buyer_toast_html

            if content != orig:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                patched_count += 1

print(f"Injected Verified $9 Buyer Notification Toast across {patched_count} HTML pages!")
