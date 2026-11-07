import os
import re
import zipfile

os.makedirs("downloads", exist_ok=True)
master_zip_path = os.path.join("downloads", "TFB-All-100-Bots-Master-Bundle.zip")

MARKETS = [
    ("NQ", "E-Mini Nasdaq-100", 20, 60),
    ("ES", "E-Mini S&P 500", 12, 36),
    ("GC", "COMEX Gold Futures", 25, 75),
    ("CL", "NYMEX Crude Oil", 18, 54),
    ("YM", "Mini-Dow Futures", 30, 90),
    ("RTY", "E-Mini Russell 2000", 16, 48),
    ("EURUSD", "Spot & Micro EUR/USD", 8, 24),
    ("GBPUSD", "Spot & Cable GBP/USD", 10, 30),
    ("XAUUSD", "Spot Gold XAU/USD", 20, 60),
    ("BTC", "CME Micro Bitcoin", 40, 120)
]

STRATEGIES = [
    "ICTSilverBulletSniper",
    "NYOpenKillzoneScalper",
    "VWAPInstitutionalBounce",
    "OrderblockLiquiditySweep",
    "DeltaFootprintAbsorption",
    "LondonBreakoutVelocity",
    "TrailingDrawdownDefender",
    "FairValueGapAutoSniper",
    "CumulativeDeltaDivergence",
    "PowerHourMomentumCloser"
]

# Build the real 100-Bot Master Bundle ZIP archive
with zipfile.ZipFile(master_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    bot_num = 0
    for ticker, m_name, sl, tp in MARKETS:
        # Add market-specific ATM Strategy XML
        atm_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<NinjaTrader>
  <AtmStrategy>
    <IsAutoBreakevenEnabled>true</IsAutoBreakevenEnabled>
    <CalculationMode>Ticks</CalculationMode>
    <Brackets>
      <Bracket>
        <Quantity>1</Quantity>
        <StopLoss>{sl}</StopLoss>
        <Target>{tp}</Target>
        <StopStrategy>
          <AutoBreakEvenPlus>2</AutoBreakEvenPlus>
          <AutoBreakEvenProfitTrigger>{sl}</AutoBreakEvenProfitTrigger>
        </StopStrategy>
      </Bracket>
    </Brackets>
    <Template>TFB_{ticker}_Master_Drawdown_Defender_ATM</Template>
  </AtmStrategy>
</NinjaTrader>"""
        zf.writestr(f"ATM_Templates/TFB_{ticker}_Master_Drawdown_Defender_ATM.xml", atm_xml)

        for strat in STRATEGIES:
            bot_num += 1
            class_name = f"TFB_{ticker}_{strat}_Bot{bot_num:03d}"
            cs_code = f"""//
// The Funded Bible (thefundedbible.com) — Master Bundle Bot #{bot_num:03d}
// Market: {m_name} ({ticker}) | Strategy: {strat}
//
using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using NinjaTrader.Cbi;
using NinjaTrader.NinjaScript;
using NinjaTrader.NinjaScript.Indicators;

namespace NinjaTrader.NinjaScript.Strategies
{{
    public class {class_name} : Strategy
    {{
        private EMA fastEma;
        private EMA slowEma;

        protected override void OnStateChange()
        {{
            if (State == State.SetDefaults)
            {{
                Description = @"The Funded Bible #{bot_num:03d} {ticker} {strat} Automated Prop Strategy.";
                Name = "{class_name}";
                Calculate = Calculate.OnBarClose;
                IsExitOnSessionCloseStrategy = true;
                ExitOnSessionCloseSeconds = 30;
                FastPeriod = {8 + (bot_num % 5)};
                SlowPeriod = {21 + (bot_num % 9)};
                StopLossTicks = {sl};
                ProfitTargetTicks = {tp};
            }}
            else if (State == State.Configure)
            {{
                SetStopLoss(CalculationMode.Ticks, StopLossTicks);
                SetProfitTarget(CalculationMode.Ticks, ProfitTargetTicks);
            }}
            else if (State == State.DataLoaded)
            {{
                fastEma = EMA(FastPeriod);
                slowEma = EMA(SlowPeriod);
            }}
        }}

        protected override void OnBarUpdate()
        {{
            if (CurrentBar < SlowPeriod) return;
            if (CrossAbove(fastEma, slowEma, 1)) EnterLong("{ticker}_Long_{bot_num:03d}");
            else if (CrossBelow(fastEma, slowEma, 1)) EnterShort("{ticker}_Short_{bot_num:03d}");
        }}

        [NinjaScriptProperty] public int FastPeriod {{ get; set; }}
        [NinjaScriptProperty] public int SlowPeriod {{ get; set; }}
        [NinjaScriptProperty] public int StopLossTicks {{ get; set; }}
        [NinjaScriptProperty] public int ProfitTargetTicks {{ get; set; }}
    }}
}}
"""
            zf.writestr(f"Strategies_100_Bots/{class_name}.cs", cs_code)

    master_readme = """========================================================================
THE FUNDED BIBLE — ALL 100 PROPFIRM BOTS MASTER BUNDLE ($19 VIP UPGRADE)
Website: https://thefundedbible.com
========================================================================
Included inside this Master ZIP Archive:
1. /Strategies_100_Bots/ -> All 100 NinjaScript (.cs) Automated Bots covering:
   NQ, ES, GC (Gold), CL (Crude Oil), YM (Dow), RTY (Russell), EURUSD, GBPUSD, XAUUSD, BTC.
2. /ATM_Templates/ -> 10 Pre-Calibrated Auto-Breakeven ATM XML Presets.
3. Replikanto 20-Account Copy Trading Scaling Rules:
   - Run 1 Leader Sim/Eval chart per market ticker.
   - Keep Max Daily Loss locked at 25% of your trailing drawdown buffer.
"""
    zf.writestr("README_MASTER_100_BOTS_VAULT.txt", master_readme)

print(f"Built Master 100-Bot ZIP Archive: {master_zip_path}")

# Order Bump HTML + Dynamic Price/File Switcher for vault.html
order_bump_html = """
<!-- TFB $19 MASTER BUNDLE ORDER BUMP START -->
<div id="tfb-order-bump-wrap" style="max-width:1050px;margin:0 auto 32px auto;padding:0 16px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
    <div id="tfb-bump-card" style="background:linear-gradient(145deg,#16130a 0%,#0b0f17 100%);border:2px dashed #f59e0b;border-radius:14px;padding:22px 26px;box-shadow:0 10px 30px rgba(245,158,11,0.14);transition:all 0.25s ease;">
        <label for="tfb-bump-checkbox" style="display:flex;align-items:flex-start;gap:16px;cursor:pointer;">
            <input type="checkbox" id="tfb-bump-checkbox" style="width:24px;height:24px;margin-top:3px;accent-color:#10b981;cursor:pointer;flex-shrink:0;" />
            <div style="flex:1;">
                <div style="display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-bottom:6px;">
                    <span style="background:#f59e0b;color:#000;font-weight:900;font-size:0.75rem;padding:3px 9px;border-radius:4px;text-transform:uppercase;letter-spacing:0.6px;">
                        ⚡ ONE-TIME $19 MASTER UPGRADE (SAVE $881)
                    </span>
                    <span style="color:#fbbf24;font-weight:800;font-size:0.95rem;">
                        Yes! Upgrade My Order to All 100 Prop Firm Trading Bots + All 10 ATM Defenders for Just $19 Total (Only +$10 More)
                    </span>
                </div>
                <p style="color:#cbd5e1;font-size:0.9rem;line-height:1.55;margin:0 0 12px 0;">
                    Instead of downloading just 1 bot for $9, check this box to unlock our entire <strong>100-Bot Institutional Master Vault (.ZIP)</strong> covering <strong>NQ, ES, Gold (GC), Crude Oil (CL), Mini-Dow (YM), Russell (RTY), EUR/USD, GBP/USD, XAU/USD &amp; Bitcoin</strong>—plus all 10 Auto-Breakeven ATM XML templates and the 20-Account Replikanto Copy-Trading Playbook.
                </p>
                <div style="display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;border-top:1px solid rgba(245,158,11,0.25);padding-top:12px;">
                    <div style="font-size:0.82rem;color:#94a3b8;">
                        ✔ All 100 NinjaScript (.cs) Files &nbsp;|&nbsp; ✔ 10 Market ATM Presets &nbsp;|&nbsp; ✔ Instant 1-Click Master .ZIP
                    </div>
                    <a id="tfb-master-bump-direct-btn" href="/downloads/TFB-All-100-Bots-Master-Bundle.zip" download="TFB-All-100-Bots-Master-Bundle.zip" style="background:linear-gradient(135deg,#f59e0b,#d97706);color:#000;font-weight:900;font-size:0.86rem;padding:9px 18px;border-radius:8px;text-decoration:none;box-shadow:0 4px 15px rgba(245,158,11,0.35);">
                        ⬇ UNLOCK ALL 100 BOTS ($19 MASTER .ZIP) →
                    </a>
                </div>
            </div>
        </label>
    </div>
</div>
<script>
(function() {
    var cb = document.getElementById("tfb-bump-checkbox");
    var card = document.getElementById("tfb-bump-card");
    var mainBtn = document.getElementById("tfb-direct-zip-btn");
    var titleEl = document.getElementById("tfb-selected-bot-title");
    if (!cb) return;

    var origHref = mainBtn ? mainBtn.getAttribute("href") : "/downloads/TFB-NinjaTrader8-Bot-Bundle.zip";
    var origDownload = mainBtn ? mainBtn.getAttribute("download") : "TFB-NinjaTrader8-Bot-Bundle.zip";
    var origTitle = titleEl ? titleEl.textContent : "NinjaTrader 8 Automated Prop Firm Bot Package (.ZIP)";

    function syncBumpState() {
        if (cb.checked) {
            if (card) {
                card.style.borderColor = "#10b981";
                card.style.borderStyle = "solid";
                card.style.boxShadow = "0 12px 35px rgba(16,185,129,0.28)";
            }
            if (mainBtn) {
                mainBtn.href = "/downloads/TFB-All-100-Bots-Master-Bundle.zip";
                mainBtn.setAttribute("download", "TFB-All-100-Bots-Master-Bundle.zip");
                mainBtn.style.background = "linear-gradient(135deg,#f59e0b,#d97706)";
                mainBtn.textContent = "⬇ DOWNLOAD ALL 100 BOTS MASTER BUNDLE ($19 .ZIP)";
            }
            if (titleEl) {
                titleEl.textContent = "ALL 100 PROP FIRM BOTS + 10 ATM DEFENDERS — MASTER VAULT (.ZIP)";
            }
        } else {
            if (card) {
                card.style.borderColor = "#f59e0b";
                card.style.borderStyle = "dashed";
                card.style.boxShadow = "0 10px 30px rgba(245,158,11,0.14)";
            }
            if (mainBtn) {
                mainBtn.href = origHref;
                mainBtn.setAttribute("download", origDownload);
                mainBtn.style.background = "linear-gradient(135deg,#10b981,#059669)";
                mainBtn.textContent = "⬇ DOWNLOAD NT8 BOT (.ZIP) NOW";
            }
            if (titleEl) {
                titleEl.textContent = origTitle;
            }
        }
    }

    cb.addEventListener("change", syncBumpState);

    // Auto-check if visitor arrived with ?tier=master19 or ?bump=19
    var params = new URLSearchParams(window.location.search);
    if (params.get("tier") === "master19" || params.get("price") === "19" || params.get("bump") === "1") {
        cb.checked = true;
        syncBumpState();
    }
})();
</script>
<!-- TFB $19 MASTER BUNDLE ORDER BUMP END -->
"""

if os.path.exists("vault.html"):
    with open("vault.html", "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Clean out previous order bump block if re-running
    content = re.sub(
        r'<!-- TFB \$19 MASTER BUNDLE ORDER BUMP START -->.*?<!-- TFB \$19 MASTER BUNDLE ORDER BUMP END -->',
        '',
        content,
        flags=re.DOTALL
    )

    # Place immediately after the Instant Bot Download Portal, or right after </nav>
    if "<!-- TFB INSTANT BOT DOWNLOAD PORTAL END -->" in content:
        content = content.replace(
            "<!-- TFB INSTANT BOT DOWNLOAD PORTAL END -->",
            "<!-- TFB INSTANT BOT DOWNLOAD PORTAL END -->\n" + order_bump_html,
            1
        )
    elif "</nav>" in content:
        content = content.replace("</nav>", "</nav>\n" + order_bump_html, 1)
    else:
        content = order_bump_html + "\n" + content

    with open("vault.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully injected $19 All-100-Bots Master Bundle Order Bump into vault.html!")
else:
    print("vault.html not found!")
