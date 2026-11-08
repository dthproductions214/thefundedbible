import os
import re

sticky_banner_html = """
<!-- TFB STICKY $9 FLASH LOCK BANNER START -->
<div id="tfb-sticky-flash-bar" style="position:sticky;top:0;z-index:99999;background:linear-gradient(90deg,#064e3b 0%,#047857 50%,#064e3b 100%);border-bottom:1px solid #10b981;padding:10px 16px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;box-shadow:0 4px 20px rgba(0,0,0,0.6);">
    <div style="max-width:1280px;margin:0 auto;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:14px;text-align:center;">
        <span style="background:#f59e0b;color:#000;font-weight:900;font-size:0.74rem;padding:3px 9px;border-radius:4px;letter-spacing:0.6px;text-transform:uppercase;">
            ⚡ 95% OFF FLASH LOCK
        </span>
        <span style="color:#f8fafc;font-size:0.9rem;font-weight:700;">
            Unlock Any Automated NinjaTrader 8 Prop Bot + ATM Drawdown Defender for <strong style="color:#34d399;text-decoration:underline;">$9.00</strong> <span style="color:#94a3b8;text-decoration:line-through;font-size:0.82rem;">$197</span> (Code: <strong style="color:#fbbf24;">BIBLE80</strong>)
        </span>
        <span id="tfb-flash-timer" style="font-family:monospace;background:rgba(0,0,0,0.45);color:#34d399;padding:3px 8px;border-radius:4px;font-size:0.85rem;font-weight:800;border:1px solid rgba(16,185,129,0.4);">
            14:59
        </span>
        <a id="tfb-flash-bar-cta" href="/vault.html?tier=bot9&price=9&promo=BIBLE80" style="background:#10b981;color:#000;font-weight:900;font-size:0.82rem;padding:6px 14px;border-radius:6px;text-decoration:none;box-shadow:0 2px 10px rgba(16,185,129,0.4);white-space:nowrap;">
            CLAIM $9 BOT ACCESS →
        </a>
    </div>
</div>
<script>
(function() {
    // Dynamically route sticky CTA to the specific bot if viewing a /bots/ page
    var path = window.location.pathname;
    var cta = document.getElementById('tfb-flash-bar-cta');
    if (cta && path.indexOf('/bots/') !== -1 && path.indexOf('.html') !== -1) {
        var slug = path.split('/').pop().replace('.html', '');
        cta.href = '/vault.html?tier=bot9&price=9&promo=BIBLE80&bot=' + encodeURIComponent(slug);
        cta.textContent = 'UNLOCK THIS BOT FOR $9 →';
    }
    // Persistent 15-minute urgency countdown per session
    var timerEl = document.getElementById('tfb-flash-timer');
    if (timerEl) {
        var key = 'tfb_flash_lock_expiry';
        var now = Math.floor(Date.now() / 1000);
        var exp = parseInt(sessionStorage.getItem(key) || '0', 10);
        if (!exp || exp <= now) {
            exp = now + 899;
            sessionStorage.setItem(key, exp.toString());
        }
        setInterval(function() {
            var rem = exp - Math.floor(Date.now() / 1000);
            if (rem <= 0) { exp = Math.floor(Date.now() / 1000) + 899; rem = 899; }
            var m = Math.floor(rem / 60);
            var s = rem % 60;
            timerEl.textContent = (m < 10 ? '0' + m : m) + ':' + (s < 10 ? '0' + s : s);
        }, 1000);
    }
})();
</script>
<!-- TFB STICKY $9 FLASH LOCK BANNER END -->
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

            # Remove any existing sticky banner block to avoid duplicates
            content = re.sub(
                r'<!-- TFB STICKY \$9 FLASH LOCK BANNER START -->.*?<!-- TFB STICKY \$9 FLASH LOCK BANNER END -->',
                '',
                content,
                flags=re.DOTALL
            )

            # Inject right after opening <body> tag so it stays pinned at the very top
            if re.search(r'<body[^>]*>', content, flags=re.IGNORECASE):
                content = re.sub(
                    r'(<body[^>]*>)',
                    r'\1\n' + sticky_banner_html,
                    content,
                    count=1,
                    flags=re.IGNORECASE
                )
            else:
                content = sticky_banner_html + "\n" + content

            if content != orig:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                patched_count += 1

print(f"Injected Sticky $9 Flash Lock Banner across {patched_count} HTML pages!")
