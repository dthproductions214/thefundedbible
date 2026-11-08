import os
import re

filter_bar_html = """
<!-- TFB CATALOG SEARCH & MARKET FILTER START -->
<div id="tfb-catalog-controls" style="max-width:1280px;margin:10px auto 24px;padding:0 20px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    <div style="background:#0f141d;border:1px solid #1e293b;border-radius:12px;padding:18px 20px;display:flex;flex-wrap:wrap;gap:16px;justify-content:space-between;align-items:center;">
        <div style="flex:1;min-width:260px;position:relative;">
            <input type="text" id="tfb-bot-search" placeholder="Search by ticker or strategy (e.g., Silver Bullet, VWAP, NQ, Gold, Drawdown)..." style="width:100%;padding:12px 16px;border-radius:8px;border:1px solid #334155;background:#07090e;color:#f8fafc;font-size:0.95rem;outline:none;" />
        </div>
        <div id="tfb-market-pills" style="display:flex;flex-wrap:wrap;gap:8px;align-items:center;">
            <button type="button" class="tfb-filter-btn active" data-filter="ALL" style="background:#10b981;color:#000;border:1px solid #10b981;padding:8px 14px;border-radius:8px;font-weight:800;font-size:0.82rem;cursor:pointer;">ALL (100)</button>
            <button type="button" class="tfb-filter-btn" data-filter="NQ" style="background:#07090e;color:#cbd5e1;border:1px solid #334155;padding:8px 12px;border-radius:8px;font-weight:700;font-size:0.82rem;cursor:pointer;">NQ</button>
            <button type="button" class="tfb-filter-btn" data-filter="ES" style="background:#07090e;color:#cbd5e1;border:1px solid #334155;padding:8px 12px;border-radius:8px;font-weight:700;font-size:0.82rem;cursor:pointer;">ES</button>
            <button type="button" class="tfb-filter-btn" data-filter="GC" style="background:#07090e;color:#cbd5e1;border:1px solid #334155;padding:8px 12px;border-radius:8px;font-weight:700;font-size:0.82rem;cursor:pointer;">GC (Gold)</button>
            <button type="button" class="tfb-filter-btn" data-filter="CL" style="background:#07090e;color:#cbd5e1;border:1px solid #334155;padding:8px 12px;border-radius:8px;font-weight:700;font-size:0.82rem;cursor:pointer;">CL (Oil)</button>
            <button type="button" class="tfb-filter-btn" data-filter="YM" style="background:#07090e;color:#cbd5e1;border:1px solid #334155;padding:8px 12px;border-radius:8px;font-weight:700;font-size:0.82rem;cursor:pointer;">YM (Dow)</button>
            <button type="button" class="tfb-filter-btn" data-filter="RTY" style="background:#07090e;color:#cbd5e1;border:1px solid #334155;padding:8px 12px;border-radius:8px;font-weight:700;font-size:0.82rem;cursor:pointer;">RTY</button>
            <button type="button" class="tfb-filter-btn" data-filter="FOREX" style="background:#07090e;color:#cbd5e1;border:1px solid #334155;padding:8px 12px;border-radius:8px;font-weight:700;font-size:0.82rem;cursor:pointer;">Forex</button>
            <button type="button" class="tfb-filter-btn" data-filter="XAUUSD" style="background:#07090e;color:#cbd5e1;border:1px solid #334155;padding:8px 12px;border-radius:8px;font-weight:700;font-size:0.82rem;cursor:pointer;">XAU/USD</button>
            <button type="button" class="tfb-filter-btn" data-filter="BTC" style="background:#07090e;color:#cbd5e1;border:1px solid #334155;padding:8px 12px;border-radius:8px;font-weight:700;font-size:0.82rem;cursor:pointer;">Bitcoin</button>
        </div>
    </div>
    <div id="tfb-filter-status" style="margin-top:10px;font-size:0.84rem;color:#94a3b8;padding-left:4px;">
        Showing <strong id="tfb-visible-count" style="color:#10b981;">100</strong> of 100 verified prop firm trading bots ($9 Flash Lock active)
    </div>
</div>
<script>
(function() {
    var searchInput = document.getElementById("tfb-bot-search");
    var buttons = document.querySelectorAll(".tfb-filter-btn");
    var cards = document.querySelectorAll(".bot-card");
    var countEl = document.getElementById("tfb-visible-count");
    var currentMarket = "ALL";

    function filterBots() {
        var query = searchInput ? searchInput.value.toLowerCase().trim() : "";
        var visible = 0;

        cards.forEach(function(card) {
            var market = (card.getAttribute("data-market") || "").toUpperCase();
            var text = (card.textContent || "").toLowerCase();

            var matchesMarket = false;
            if (currentMarket === "ALL") {
                matchesMarket = true;
            } else if (currentMarket === "FOREX") {
                matchesMarket = (market === "EURUSD" || market === "GBPUSD");
            } else {
                matchesMarket = (market === currentMarket);
            }

            var matchesSearch = !query || text.indexOf(query) !== -1;

            if (matchesMarket && matchesSearch) {
                card.style.display = "flex";
                visible++;
            } else {
                card.style.display = "none";
            }
        });

        if (countEl) countEl.textContent = visible.toString();
    }

    buttons.forEach(function(btn) {
        btn.addEventListener("click", function() {
            buttons.forEach(function(b) {
                b.style.background = "#07090e";
                b.style.color = "#cbd5e1";
                b.style.borderColor = "#334155";
                b.style.fontWeight = "700";
            });
            btn.style.background = "#10b981";
            btn.style.color = "#000000";
            btn.style.borderColor = "#10b981";
            btn.style.fontWeight = "800";

            currentMarket = btn.getAttribute("data-filter") || "ALL";
            filterBots();
        });
    });

    if (searchInput) {
        searchInput.addEventListener("input", filterBots);
    }
})();
</script>
<!-- TFB CATALOG SEARCH & MARKET FILTER END -->
"""

if os.path.exists("bots-catalog.html"):
    with open("bots-catalog.html", "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Remove existing filter block if re-running
    content = re.sub(
        r'<!-- TFB CATALOG SEARCH & MARKET FILTER START -->.*?<!-- TFB CATALOG SEARCH & MARKET FILTER END -->',
        '',
        content,
        flags=re.DOTALL
    )

    # Inject directly above <div class="grid">
    if '<div class="grid">' in content:
        content = content.replace('<div class="grid">', filter_bar_html + '\n    <div class="grid">', 1)
    else:
        content = content + "\n" + filter_bar_html

    with open("bots-catalog.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully injected Interactive Search & Market Filter Bar into bots-catalog.html!")
else:
    print("bots-catalog.html not found!")
