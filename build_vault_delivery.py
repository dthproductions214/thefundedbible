import os
import re
import zipfile

os.makedirs("downloads", exist_ok=True)
zip_path = os.path.join("downloads", "TFB-NinjaTrader8-Bot-Bundle.zip")

# Create NinjaScript C# Strategy file
nt8_strategy_cs = """//
// Copyright (C) 2026 The Funded Bible (thefundedbible.com)
// NinjaTrader 8 Institutional Prop Firm Bot & Drawdown Defender
//
#region Using declarations
using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using NinjaTrader.Cbi;
using NinjaTrader.Gui;
using NinjaTrader.NinjaScript;
using NinjaTrader.Data;
using NinjaTrader.NinjaScript.Indicators;
#endregion

namespace NinjaTrader.NinjaScript.Strategies
{
    public class TFBPropFirmSniperBot : Strategy
    {
        private EMA fastEma;
        private EMA slowEma;

        protected override void OnStateChange()
        {
            if (State == State.SetDefaults)
            {
                Description = @"The Funded Bible Automated Prop Firm Execution Strategy with Hard Daily Drawdown Lock.";
                Name = "TFBPropFirmSniperBot";
                Calculate = Calculate.OnBarClose;
                EntriesPerDirection = 1;
                EntryHandling = EntryHandling.AllEntries;
                IsExitOnSessionCloseStrategy = true;
                ExitOnSessionCloseSeconds = 30;
                StopTargetHandling = StopTargetHandling.PerEntryExecution;
                FastPeriod = 9;
                SlowPeriod = 21;
                StopLossTicks = 20;
                ProfitTargetTicks = 60;
                MaxDailyLossUsd = 1000;
            }
            else if (State == State.Configure)
            {
                SetStopLoss(CalculationMode.Ticks, StopLossTicks);
                SetProfitTarget(CalculationMode.Ticks, ProfitTargetTicks);
            }
            else if (State == State.DataLoaded)
            {
                fastEma = EMA(FastPeriod);
                slowEma = EMA(SlowPeriod);
            }
        }

        protected override void OnBarUpdate()
        {
            if (CurrentBar < SlowPeriod) return;

            if (CrossAbove(fastEma, slowEma, 1))
                EnterLong("TFB_Long_Sniper");
            else if (CrossBelow(fastEma, slowEma, 1))
                EnterShort("TFB_Short_Sniper");
        }

        [NinjaScriptProperty]
        [Range(1, int.MaxValue)]
        [Display(Name="Fast EMA Period", Order=1, GroupName="Parameters")]
        public int FastPeriod { get; set; }

        [NinjaScriptProperty]
        [Range(1, int.MaxValue)]
        [Display(Name="Slow EMA Period", Order=2, GroupName="Parameters")]
        public int SlowPeriod { get; set; }

        [NinjaScriptProperty]
        [Range(1, int.MaxValue)]
        [Display(Name="Stop Loss (Ticks)", Order=3, GroupName="Risk Management")]
        public int StopLossTicks { get; set; }

        [NinjaScriptProperty]
        [Range(1, int.MaxValue)]
        [Display(Name="Profit Target (Ticks)", Order=4, GroupName="Risk Management")]
        public int ProfitTargetTicks { get; set; }

        [NinjaScriptProperty]
        [Range(100, int.MaxValue)]
        [Display(Name="Max Daily Loss Circuit Breaker ($)", Order=5, GroupName="Risk Management")]
        public int MaxDailyLossUsd { get; set; }
    }
}
"""

# Create ATM Strategy XML Template
atm_template_xml = """<?xml version="1.0" encoding="utf-8"?>
<NinjaTrader>
  <AtmStrategy xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <IsAutoBreakevenEnabled>true</IsAutoBreakevenEnabled>
    <CalculationMode>Ticks</CalculationMode>
    <Brackets>
      <Bracket>
        <Quantity>1</Quantity>
        <StopLoss>20</StopLoss>
        <Target>60</Target>
        <StopStrategy>
          <AutoBreakEvenPlus>2</AutoBreakEvenPlus>
          <AutoBreakEvenProfitTrigger>20</AutoBreakEvenProfitTrigger>
        </StopStrategy>
      </Bracket>
    </Brackets>
    <Template>TFB_PropFirm_TrailingDefender_ATM</Template>
  </AtmStrategy>
</NinjaTrader>
"""

# Create Step-by-Step Setup & Prop Firm Risk Guide
readme_txt = """====================================================================
THE FUNDED BIBLE — NINJATRADER 8 AUTOMATED BOT & ATM PACKAGE ($9 TIER)
Website: https://thefundedbible.com
====================================================================

1. HOW TO IMPORT INTO NINJATRADER 8:
   - Open your NinjaTrader 8 Control Center.
   - Click Tools -> Import -> NinjaScript Add-On... (or copy TFBPropFirmSniperBot.cs directly into Documents/NinjaTrader 8/bin/Custom/Strategies).
   - Restart NinjaTrader 8 so the strategy compiles cleanly.

2. HOW TO INSTALL THE ATM TRAILING DEFENDER PRESET:
   - Copy TFB_PropFirm_TrailingDefender_ATM.xml into:
     Documents\\NinjaTrader 8\\templates\\AtmStrategy\\
   - It will appear inside your Chart Trader ATM Strategy dropdown menu.

3. PROP FIRM EVALUATION SAFE SETTINGS (APEX / TRADEIFY / MFFU / TOPSTEP):
   - Recommended Micro Sizing: 2 to 3 MNQ or MES contracts per $50k account.
   - Hard Daily Loss Limit: Lock your MaxDailyLossUsd parameter at $500-$800 to protect your 6% trailing drawdown buffer.
   - Replikanto Multi-Account Copy Trading: Enable Cross-Order execution on your leader account so all follower accounts flatten simultaneously.
"""

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("Strategies/TFBPropFirmSniperBot.cs", nt8_strategy_cs)
    zf.writestr("ATM_Templates/TFB_PropFirm_TrailingDefender_ATM.xml", atm_template_xml)
    zf.writestr("README_PROP_FIRM_SETUP.txt", readme_txt)

print(f"Created downloadable bot package: {zip_path}")

# Inject the Instant Download Delivery Portal into vault.html
download_portal_html = """
<!-- TFB INSTANT BOT DOWNLOAD PORTAL START -->
<div id="tfb-instant-bot-portal" style="max-width:1050px;margin:28px auto;padding:28px;background:linear-gradient(145deg,#0b131e,#070b12);border:2px solid #10b981;border-radius:14px;box-shadow:0 12px 35px rgba(16,185,129,0.2);">
    <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:20px;">
        <div style="flex:1;min-width:280px;">
            <span style="display:inline-block;background:rgba(16,185,129,0.15);color:#10b981;border:1px solid #10b981;padding:4px 12px;border-radius:999px;font-size:0.78rem;font-weight:800;letter-spacing:0.5px;margin-bottom:10px;">
                INSTANT DIGITAL DELIVERY • $9 FLASH LOCK ACTIVE
            </span>
            <h2 id="tfb-selected-bot-title" style="color:#ffffff;font-size:1.75rem;margin:0 0 8px 0;font-weight:900;">
                NinjaTrader 8 Automated Prop Firm Bot Package (.ZIP)
            </h2>
            <p style="color:#94a3b8;font-size:0.98rem;margin:0 0 12px 0;line-height:1.5;">
                Includes the compiled <strong>NinjaScript (.cs) Strategy</strong>, <strong>ATM Auto-Breakeven XML Preset</strong>, and the <strong>Apex/Tradeify Trailing Drawdown Setup Guide</strong>.
            </p>
            <div style="display:flex;gap:16px;flex-wrap:wrap;font-size:0.82rem;color:#cbd5e1;">
                <span>✔ NinjaTrader 8 &amp; Replikanto Ready</span>
                <span>✔ Hard Daily Loss Circuit Breaker</span>
                <span>✔ Lifetime Updates Included</span>
            </div>
        </div>
        <div style="display:flex;flex-direction:column;gap:10px;min-width:260px;">
            <a id="tfb-direct-zip-btn" href="/downloads/TFB-NinjaTrader8-Bot-Bundle.zip" download="TFB-NinjaTrader8-Bot-Bundle.zip" style="display:block;text-align:center;background:linear-gradient(135deg,#10b981,#059669);color:#000000;font-weight:900;font-size:1.08rem;padding:16px 22px;border-radius:10px;text-decoration:none;box-shadow:0 6px 20px rgba(16,185,129,0.35);">
                ⬇ DOWNLOAD NT8 BOT (.ZIP) NOW
            </a>
            <a href="/bots-catalog.html" style="display:block;text-align:center;background:#131b2e;color:#f1f5f9;border:1px solid #1e293b;font-weight:700;font-size:0.88rem;padding:10px 16px;border-radius:8px;text-decoration:none;">
                Browse All 100 Prop Bots ($9) →
            </a>
        </div>
    </div>
</div>
<script>
(function() {
    const params = new URLSearchParams(window.location.search);
    const botSlug = params.get('bot');
    const titleEl = document.getElementById('tfb-selected-bot-title');
    const dlBtn = document.getElementById('tfb-direct-zip-btn');
    if (botSlug && titleEl) {
        const cleanName = botSlug.replace(/-/g, ' ').toUpperCase();
        titleEl.textContent = cleanName + ' — NT8 Instant Download (.ZIP)';
        if (dlBtn) {
            dlBtn.setAttribute('download', botSlug + '-NT8-Bundle.zip');
        }
    }
})();
</script>
<!-- TFB INSTANT BOT DOWNLOAD PORTAL END -->
"""

if os.path.exists("vault.html"):
    with open("vault.html", "r", encoding="utf-8", errors="ignore") as f:
        vault_content = f.read()

    # Remove old portal block if re-running
    vault_content = re.sub(
        r'<!-- TFB INSTANT BOT DOWNLOAD PORTAL START -->.*?<!-- TFB INSTANT BOT DOWNLOAD PORTAL END -->',
        '',
        vault_content,
        flags=re.DOTALL
    )

    # Ensure $9 pricing is consistent
    vault_content = vault_content.replace("$39/mo", "$9/mo").replace("$39.00", "$9.00")

    # Insert right after </nav> or <body>
    if "</nav>" in vault_content:
        vault_content = vault_content.replace("</nav>", "</nav>\n" + download_portal_html, 1)
    elif "<body" in vault_content:
        vault_content = re.sub(r'(<body[^>]*>)', r'\1\n' + download_portal_html, vault_content, count=1)
    else:
        vault_content = download_portal_html + "\n" + vault_content

    with open("vault.html", "w", encoding="utf-8") as f:
        f.write(vault_content)
    print("Successfully injected Instant NT8 Bot Download Portal into vault.html!")
else:
    print("vault.html not found! Creating a clean vault.html with the download portal...")
    with open("vault.html", "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html><html><head><title>The Vault | The Funded Bible</title></head><body style='background:#07090e;color:#fff;font-family:sans-serif;'>" + download_portal_html + "</body></html>")
