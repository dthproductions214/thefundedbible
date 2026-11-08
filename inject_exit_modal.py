import os
import re

exit_modal_html = """
<!-- TFB EXIT INTENT MODAL START -->
<style>
#tfb-exit-overlay {
    position: fixed;
    inset: 0;
    z-index: 100000;
    background: rgba(3, 6, 12, 0.85);
    backdrop-filter: blur(6px);
    display: none;
    align-items: center;
    justify-content: center;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
#tfb-exit-overlay.tfb-modal-active {
    display: flex;
    animation: tfbFadeIn 0.25s ease-out forwards;
}
@keyframes tfbFadeIn {
    from { opacity: 0; transform: scale(0.96); }
    to { opacity: 1; transform: scale(1); }
}
.tfb-exit-card {
    background: linear-gradient(145deg, #0d1522 0%, #070b12 100%);
    border: 2px solid #10b981;
    border-radius: 16px;
    max-width: 520px;
    width: 100%;
    padding: 32px 28px;
    position: relative;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), 0 0 35px rgba(16, 185, 129, 0.25);
    text-align: center;
    color: #f8fafc;
}
.tfb-exit-close {
    position: absolute;
    top: 14px;
    right: 16px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid #1e293b;
    color: #94a3b8;
    width: 32px;
    height: 32px;
    border-radius: 8px;
    font-size: 1.2rem;
    cursor: pointer;
    line-height: 1;
}
.tfb-exit-close:hover {
    color: #fff;
    border-color: #10b981;
}
.tfb-exit-badge {
    display: inline-block;
    background: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
    border: 1px solid #f59e0b;
    font-size: 0.76rem;
    font-weight: 900;
    padding: 5px 12px;
    border-radius: 999px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.tfb-exit-input {
    width: 100%;
    padding: 14px 16px;
    border-radius: 8px;
    border: 1px solid #334155;
    background: #05080f;
    color: #fff;
    font-size: 0.98rem;
    margin-bottom: 12px;
    outline: none;
}
.tfb-exit-input:focus {
    border-color: #10b981;
}
.tfb-exit-submit {
    width: 100%;
    background: linear-gradient(135deg, #10b981, #059669);
    color: #000;
    font-weight: 900;
    font-size: 1.05rem;
    padding: 15px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.35);
    transition: transform 0.15s ease;
}
.tfb-exit-submit:hover {
    transform: translateY(-2px);
}
</style>

<div id="tfb-exit-overlay" role="dialog" aria-modal="true">
    <div class="tfb-exit-card">
        <button class="tfb-exit-close" id="tfb-exit-close-btn" title="Close">×</button>
        <span class="tfb-exit-badge">⚠️ WAIT — DON'T BLOW YOUR NEXT EVALUATION</span>
        <h2 id="tfb-exit-headline" style="font-size:1.65rem;line-height:1.25;margin:0 0 10px 0;font-weight:900;">
            Lock In Any NinjaTrader 8 Bot + ATM Drawdown Defender for <span style="color:#10b981;">$9.00</span>
        </h2>
        <p style="color:#94a3b8;font-size:0.94rem;line-height:1.55;margin:0 0 18px 0;">
            Enter your best email to receive the <strong>Free Prop Firm Trailing Drawdown Cheat Sheet</strong> + instant access to our <strong style="color:#fbbf24;">$9 Flash Lock (95% Off $197)</strong> before this tab closes.
        </p>
        <form id="tfb-exit-lead-form" style="margin-bottom:12px;">
            <input type="email" id="tfb-exit-email" class="tfb-exit-input" placeholder="Enter your best trading email..." required />
            <button type="submit" id="tfb-exit-submit-btn" class="tfb-exit-submit">
                SEND BONUS &amp; UNLOCK $9 BOT ACCESS →
            </button>
        </form>
        <div style="margin-top:10px;">
            <a id="tfb-exit-direct-link" href="/vault.html?tier=bot9&price=9&promo=BIBLE80" style="color:#cbd5e1;font-size:0.82rem;text-decoration:underline;">
                Skip email &amp; go straight to the $9 Bot Download Vault →
            </a>
        </div>
        <div style="margin-top:16px;padding-top:12px;border-top:1px solid #1e293b;display:flex;justify-content:center;gap:16px;font-size:0.75rem;color:#64748b;">
            <span>🔒 Instant .ZIP Delivery</span>
            <span>⚡ Works on Apex, Tradeify &amp; MFFU</span>
        </div>
    </div>
</div>

<script>
(function() {
    var overlay = document.getElementById("tfb-exit-overlay");
    var closeBtn = document.getElementById("tfb-exit-close-btn");
    var form = document.getElementById("tfb-exit-lead-form");
    var emailInput = document.getElementById("tfb-exit-email");
    var submitBtn = document.getElementById("tfb-exit-submit-btn");
    var directLink = document.getElementById("tfb-exit-direct-link");
    var headline = document.getElementById("tfb-exit-headline");
    if (!overlay) return;

    var storageKey = "tfb_exit_modal_shown_v1";
    var targetUrl = "/vault.html?tier=bot9&price=9&promo=BIBLE80";
    var path = window.location.pathname;

    if (path.indexOf("/bots/") !== -1 && path.indexOf(".html") !== -1) {
        var slug = path.split("/").pop().replace(".html", "");
        targetUrl = "/vault.html?tier=bot9&price=9&promo=BIBLE80&bot=" + encodeURIComponent(slug);
        if (directLink) directLink.href = targetUrl;
        if (headline) {
            var cleanBot = slug.replace(/-/g, " ").toUpperCase();
            headline.innerHTML = 'Wait! Grab <span style="color:#10b981;">' + cleanBot + '</span> + Bonus ATM Preset for <span style="color:#fbbf24;">$9.00</span>';
        }
    }

    function showModal() {
        if (sessionStorage.getItem(storageKey)) return;
        sessionStorage.setItem(storageKey, "1");
        overlay.classList.add("tfb-modal-active");
    }

    function hideModal() {
        overlay.classList.remove("tfb-modal-active");
    }

    // Trigger 1: Desktop cursor moves toward top tab bar to close/leave
    document.addEventListener("mouseout", function(e) {
        if (!e.relatedTarget && e.clientY <= 12) {
            showModal();
        }
    });

    // Trigger 2: Mobile / Idle fallback after 38 seconds if not triggered yet
    setTimeout(function() {
        showModal();
    }, 38000);

    if (closeBtn) closeBtn.addEventListener("click", hideModal);
    overlay.addEventListener("click", function(e) {
        if (e.target === overlay) hideModal();
    });

    if (form) {
        form.addEventListener("submit", function(e) {
            e.preventDefault();
            var email = emailInput ? emailInput.value.trim() : "";
            if (!email) return;
            if (submitBtn) submitBtn.textContent = "UNLOCKING $9 VAULT...";

            try {
                localStorage.setItem("tfb_captured_lead_email", email);
                fetch("/api/capture-lead", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        email: email,
                        source: "exit_intent_modal_bot9",
                        page: window.location.pathname,
                        promo: "BIBLE80"
                    })
                }).catch(function() {});
            } catch (err) {}

            setTimeout(function() {
                window.location.href = targetUrl + "&email=" + encodeURIComponent(email);
            }, 350);
        });
    }
})();
</script>
<!-- TFB EXIT INTENT MODAL END -->
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
            # Remove any previous exit-intent modal block so re-runs stay clean
            content = re.sub(
                r'<!-- TFB EXIT INTENT MODAL START -->.*?<!-- TFB EXIT INTENT MODAL END -->',
                '',
                content,
                flags=re.DOTALL
            )

            # Inject right before </body>
            if "</body>" in content:
                content = content.replace("</body>", exit_modal_html + "\n</body>", 1)
            else:
                content = content + "\n" + exit_modal_html

            if content != orig:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                patched_count += 1

print(f"Injected Exit-Intent $9 Lead Capture Modal across {patched_count} HTML pages!")
