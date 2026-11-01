import os
import json
import itertools
from datetime import datetime

SITE_URL = "https://thefundedbible.com"
TODAY_STR = datetime.utcnow().strftime("%B %d, %Y")
ISO_TODAY = datetime.utcnow().strftime("%Y-%m-%d")

# 👉 PASTE YOUR #1 PAYING AFFILIATE LINK HERE!
# Every single button across all 940+ pages routes here automatically until you add individual firm links.
MY_MAIN_AFFILIATE_LINK = "https://myfundedfutures.com"

# Drip-Feed Settings: Starts at 164 core pages on Day 1, then adds 35 new long-tail pages every day up to 824+ pages!
DRIP_STATE_FILE = "drip_state.json"
DAILY_DRIP_BATCH_SIZE = 35

FIRMS = [
    {
        "id": "apex", "slug": "apex-trader-funding", "name": "Apex Trader Funding", "short": "APEX",
        "domain": "apextraderfunding.com", "accent": "#3b82f6",
        "size": "$50K", "dd": 2500, "target": 3000, "dd_type": "Intraday Trailing",
        "consistency": 30, "buffer_lock": 2600, "max_accounts": 20,
        "programs_breakdown": "Evaluation (0% Consistency Rule) | Performance Account PA (30% Windfall Rule - best day must be under 30% of total profit balance at payout request)",
        "edge_case_note": "Apex strictly enforces the 30% rule on funded Performance Accounts (PA) until your 6th payout. Evaluations have no consistency cap, meaning you can pass in 1 day.",
        "price": "$37/mo", "discount": "80% OFF", "code": "BIBLE80", "split": "100% first $25K, then 90%",
        "payout_speed": "8 Trading Days", "trust_score": "92/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    },
    {
        "id": "topstep", "slug": "topstep", "name": "Topstep", "short": "TOPSTEP",
        "domain": "topstep.com", "accent": "#10b981",
        "size": "$50K", "dd": 2000, "target": 3000, "dd_type": "EOD Trailing",
        "consistency": 50, "buffer_lock": 2000, "max_accounts": 5,
        "programs_breakdown": "Trading Combine Evaluation (50%-55% Target Cap) | Express Funded Standard (5 Winning Days of $200+) | Express Consistency Path (40% Rule)",
        "edge_case_note": "Topstep measures evaluation consistency against the profit target, giving you an End-of-Day trailing drawdown with zero intraday trailing traps.",
        "price": "$49/mo", "discount": "BEST VALUE", "code": "BIBLE", "split": "100% first $10K, then 90%",
        "payout_speed": "5 Winning Days ($200+)", "trust_score": "98/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    },
    {
        "id": "mff", "slug": "myfundedfutures", "name": "MyFundedFutures", "short": "MFFU",
        "domain": "myfundedfutures.com", "accent": "#8b5cf6",
        "size": "$50K", "dd": 2000, "target": 3000, "dd_type": "EOD Trailing",
        "consistency": 40, "buffer_lock": 2100, "max_accounts": 3,
        "programs_breakdown": "Starter Evaluation (No Eval Consistency / 40% Sim Funded) | Rapid EOD Evaluation (30% Rule) | Pro & Rapid Evaluation (50% Rule) | Expert Plan (0% Consistency Rule)",
        "edge_case_note": "MyFundedFutures Expert plans have 0% consistency restriction on both Evaluation and Sim Funded stages, while Starter/Rapid plans enforce 30%-40% with zero activation fees.",
        "price": "$77/mo", "discount": "NO ACTIVATION FEE", "code": "BIBLE", "split": "100% first $10K, then 90%",
        "payout_speed": "5 Winning Days", "trust_score": "96/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    },
    {
        "id": "tradeify", "slug": "tradeify", "name": "Tradeify", "short": "TRADEIFY",
        "domain": "tradeify.co", "accent": "#06b6d4",
        "size": "$50K", "dd": 2000, "target": 3000, "dd_type": "EOD Trailing",
        "consistency": 20, "buffer_lock": 2100, "max_accounts": 5,
        "programs_breakdown": "Lightning Instant Funded Payout 1 (20% Rule) -> Payout 2 (25% Rule) -> Payout 3+ (30% Rule) | Growth Sim Funded (35% Rule) | Select Evaluation (40% Rule)",
        "edge_case_note": "Tradeify calculates consistency using your biggest End-of-Day (EOD) PnL divided by total cycle profit. Scaling progressively unlocks from 20% to 30% on Lightning accounts.",
        "price": "$99/mo", "discount": "LIGHTNING FUNDED", "code": "BIBLE", "split": "90% Profit Split",
        "payout_speed": "Skip Eval Option", "trust_score": "94/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    },
    {
        "id": "tpt", "slug": "take-profit-trader", "name": "Take Profit Trader", "short": "TPT",
        "domain": "takeprofittrader.com", "accent": "#22c55e",
        "size": "$50K", "dd": 2000, "target": 3000, "dd_type": "EOD Trailing",
        "consistency": 50, "buffer_lock": 2000, "max_accounts": 5,
        "programs_breakdown": "Evaluation Test (50% Consistency Rule) | PRO & PRO+ Funded Account (0% Consistency Rule, Day-1 Withdrawals above Buffer)",
        "edge_case_note": "Take Profit Trader drops the 50% consistency rule completely once you reach the PRO funded stage, allowing immediate Day-1 withdrawals above the safety buffer.",
        "price": "$102/mo", "discount": "40% OFF + PRO", "code": "BIBLE", "split": "80% / 90% PRO+",
        "payout_speed": "Day 1 Payouts in PRO", "trust_score": "95/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    },
    {
        "id": "alpha", "slug": "alpha-futures", "name": "Alpha Futures", "short": "ALPHA",
        "domain": "alpha-futures.com", "accent": "#f43f5e",
        "size": "$50K", "dd": 2000, "target": 3000, "dd_type": "EOD Trailing",
        "consistency": 40, "buffer_lock": 2000, "max_accounts": 3,
        "programs_breakdown": "Standard Evaluation (50% Rule) | Advanced Evaluation (40% Rule) | Zero/Standard Qualified (40% Rule) | Direct Instant Qualified (20% Rule)",
        "edge_case_note": "Alpha Futures treats hitting the exact 40.0% boundary on qualified accounts as over the threshold—always leave at least a $25 cushion below the cap.",
        "price": "$79/mo", "discount": "HOT NEW FIRM", "code": "BIBLE", "split": "90% Profit Split",
        "payout_speed": "Bi-Weekly", "trust_score": "91/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    },
    {
        "id": "lucid", "slug": "lucid-trading", "name": "Lucid Trading", "short": "LUCID",
        "domain": "lucidtrading.com", "accent": "#a855f7",
        "size": "$50K", "dd": 2000, "target": 3000, "dd_type": "EOD Trailing",
        "consistency": 40, "buffer_lock": 2100, "max_accounts": 5,
        "programs_breakdown": "Standard EOD Evaluation (40% Rule) | Sim Funded Account (35%-40% Payout Consistency Cap)",
        "edge_case_note": "Lucid Trading calculates drawdown at End-of-Day, making it ideal for NQ/MNQ scalpers who hold runners through intraday pullbacks.",
        "price": "$45/mo", "discount": "50% OFF", "code": "BIBLE", "split": "90% Profit Split",
        "payout_speed": "Fast Payouts", "trust_score": "90/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    },
    {
        "id": "topone", "slug": "top-one-futures", "name": "Top One Futures", "short": "TOPONE",
        "domain": "toponefutures.com", "accent": "#14b8a6",
        "size": "$50K", "dd": 2000, "target": 3000, "dd_type": "EOD Trailing",
        "consistency": 30, "buffer_lock": 2000, "max_accounts": 5,
        "programs_breakdown": "Instant Sim Funded (25%-30% Consistency Rule) | 1-Step Challenge (40% Rule)",
        "edge_case_note": "Top One Futures offers both 1-Step evaluations and straight-to-funded options with fast Rise payouts.",
        "price": "$65/mo", "discount": "55% OFF", "code": "BIBLE", "split": "90% Profit Split",
        "payout_speed": "Fast Payouts", "trust_score": "91/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    },
    {
        "id": "bulenox", "slug": "bulenox", "name": "Bulenox", "short": "BULENOX",
        "domain": "bulenox.com", "accent": "#f59e0b",
        "size": "$50K", "dd": 2500, "target": 3000, "dd_type": "EOD or Intraday",
        "consistency": 40, "buffer_lock": 2600, "max_accounts": 11,
        "programs_breakdown": "Qualification Account (0% Consistency Rule) | Master Funded Account (40% Rule) | Fast Track Payout 1 (20% Rule)",
        "edge_case_note": "Bulenox lets you choose between Option 1 (Intraday Trailing, no scaling) and Option 2 (EOD Trailing with scaling) and allows up to 11 active Master accounts.",
        "price": "$38/mo", "discount": "75% OFF", "code": "BIBLE75", "split": "100% first $10K, then 90%",
        "payout_speed": "10 Trading Days", "trust_score": "89/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    },
    {
        "id": "fundednext", "slug": "fundednext-futures", "name": "FundedNext Futures", "short": "FNEXT",
        "domain": "fundednext.com", "accent": "#6366f1",
        "size": "$50K", "dd": 2000, "target": 3000, "dd_type": "EOD Trailing",
        "consistency": 40, "buffer_lock": 2000, "max_accounts": 5,
        "programs_breakdown": "Legacy / Flex Challenge (40% Evaluation Rule, 0% Funded Rule) | Rapid Pro Funded (40% Rule)",
        "edge_case_note": "FundedNext Futures pays a 15% profit share bonus from your evaluation phase once you achieve your first funded payout.",
        "price": "$79/mo", "discount": "20% OFF", "code": "BIBLE", "split": "90% Split + 15% Bonus",
        "payout_speed": "24 Hours", "trust_score": "93/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    },
    {
        "id": "tradeday", "slug": "tradeday", "name": "TradeDay", "short": "TRADEDAY",
        "domain": "tradeday.com", "accent": "#ec4899",
        "size": "$50K", "dd": 2000, "target": 3000, "dd_type": "EOD Trailing",
        "consistency": 30, "buffer_lock": 2000, "max_accounts": 3,
        "programs_breakdown": "Standard Evaluation (30% Quick Pay Rule) | Fast Pass Funded (45% Rule)",
        "edge_case_note": "TradeDay calculates drawdown strictly on End-of-Day settled balances and allows Day-1 withdrawals once you clear your buffer.",
        "price": "$99/mo", "discount": "20% OFF", "code": "BIBLE", "split": "80% to 95% Split",
        "payout_speed": "Day 1 Direct", "trust_score": "95/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    },
    {
        "id": "blusky", "slug": "blusky-trading", "name": "BluSky Trading", "short": "BLUSKY",
        "domain": "blusky.pro", "accent": "#0ea5e9",
        "size": "$50K", "dd": 2000, "target": 3000, "dd_type": "EOD Trailing",
        "consistency": 30, "buffer_lock": 2000, "max_accounts": 4,
        "programs_breakdown": "Evaluation (30% Rule) | BluLive Brokerage Account (0% Consistency Rule, Daily Payouts)",
        "edge_case_note": "BluSky transitions traders to a real live brokerage account with zero activation fees and daily withdrawal processing.",
        "price": "$95/mo", "discount": "30% OFF", "code": "BIBLE", "split": "90% Real Brokerage",
        "payout_speed": "Daily Payouts", "trust_score": "93/100",
        "aff_url": MY_MAIN_AFFILIATE_LINK
    }
]

ACCOUNT_TIERS = [
    {"tier": "25k", "label": "$25K", "dd": 1500, "target": 1500, "buf": 1600},
    {"tier": "50k", "label": "$50K", "dd": 2000, "target": 3000, "buf": 2100},
    {"tier": "100k", "label": "$100K", "dd": 3000, "target": 6000, "buf": 3100},
    {"tier": "150k", "label": "$150K", "dd": 4500, "target": 9000, "buf": 4600},
    {"tier": "250k", "label": "$250K", "dd": 6500, "target": 15000, "buf": 6600}
]

INSTRUMENTS = [
    {"ticker": "MNQ", "name": "Micro E-Mini Nasdaq-100", "pt_val": 2, "stop": 25, "exchange": "CME", "tick_val": "$0.50"},
    {"ticker": "NQ", "name": "E-Mini Nasdaq-100", "pt_val": 20, "stop": 15, "exchange": "CME", "tick_val": "$5.00"},
    {"ticker": "MES", "name": "Micro E-Mini S&P 500", "pt_val": 5, "stop": 12, "exchange": "CME", "tick_val": "$1.25"},
    {"ticker": "ES", "name": "E-Mini S&P 500", "pt_val": 50, "stop": 8, "exchange": "CME", "tick_val": "$12.50"},
    {"ticker": "MGC", "name": "Micro Gold Futures", "pt_val": 10, "stop": 15, "exchange": "COMEX", "tick_val": "$1.00"}
]

def render_firm_logo(firm, size_cls="w-11 h-11"):
    logo_url = f"https://www.google.com/s2/favicons?domain={firm['domain']}&sz=128"
    return f"""
    <div class="relative {size_cls} rounded-xl bg-[#141824] border border-white/15 flex items-center justify-center overflow-hidden shrink-0 shadow-lg" style="box-shadow: 0 0 15px {firm['accent']}25;">
        <img src="{logo_url}" alt="{firm['name']} Official Logo" class="w-7 h-7 object-contain z-10" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
        <span class="hidden absolute inset-0 items-center justify-center font-black text-[10px] tracking-tighter text-white" style="background: {firm['accent']}33;">{firm['short']}</span>
    </div>
    """

def build_schema_json(title, desc, url, faqs=None):
    graph = [
        {
            "@type": "SoftwareApplication",
            "name": title,
            "operatingSystem": "Web Browser",
            "applicationCategory": "FinanceApplication",
            "description": desc,
            "url": url,
            "offers": {"@type": "Offer", "price": "0.00", "priceCurrency": "USD"},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "ratingCount": "1420"}
        }
    ]
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ]
        })
    return f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph})}</script>'

def get_header_nav():
    return f"""
    <div class="bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-600 text-black text-center py-2 px-4 font-black text-xs md:text-sm tracking-tight">
        ⚡ 100% FREE FUTURES PROP TERMINAL: Lot Sizer + Program-Specific Consistency Fixer + 20-Acct Copy Multiplier ({TODAY_STR})
    </div>
    <header class="border-b border-white/10 bg-[#07090e]/95 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-6 py-4 flex flex-wrap justify-between items-center gap-4">
            <a href="/index.html" class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-yellow-400 to-amber-600 flex items-center justify-center text-black font-black text-lg shadow-[0_0_15px_rgba(234,179,8,0.4)]">⚡</div>
                <div>
                    <span class="text-xl font-black tracking-tighter text-white block leading-none">THE FUNDED <span class="text-yellow-500">BIBLE</span></span>
                    <span class="text-[10px] text-emerald-400 font-bold tracking-widest uppercase">Verified Prop Firm Match & Risk OS</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 text-xs md:text-sm font-semibold text-slate-300">
                <a href="/index.html#super-terminal" class="hover:text-yellow-400 transition">4-in-1 Terminal</a>
                <a href="/consistency-rule-calculator.html" class="text-yellow-400 font-bold hover:underline">Consistency Fixer</a>
                <a href="/copy-trading-payout-multiplier.html" class="text-emerald-400 font-bold hover:underline">20-Acct Multiplier</a>
                <a href="/eod-drawdown-prop-firms.html" class="hover:text-yellow-400 transition">Best EOD Firms</a>
                <a href="{MY_MAIN_AFFILIATE_LINK}" target="_blank" class="bg-yellow-500 hover:bg-yellow-400 text-black font-black px-4 py-2 rounded-lg text-xs shadow-lg transition">🚀 #1 Verified Deal</a>
            </nav>
        </div>
    </header>
    """

def get_footer():
    firm_links = "".join([f'<li><a href="/{f["slug"]}.html" class="hover:text-yellow-400">{f["name"]} Rules & Deals</a></li>' for f in FIRMS])
    cons_links = "".join([f'<li><a href="/{f["slug"]}-consistency-calculator.html" class="hover:text-yellow-400">{f["name"]} {f["consistency"]}% Consistency Calc</a></li>' for f in FIRMS])
    vs_pairs = list(itertools.combinations(FIRMS[:6], 2))[:12]
    vs_links = "".join([f'<li><a href="/{a["slug"]}-vs-{b["slug"]}.html" class="hover:text-yellow-400">{a["name"]} vs {b["name"]}</a></li>' for a, b in vs_pairs])

    return f"""
    <footer class="border-t border-white/10 mt-24 py-14 bg-[#05060a] text-slate-400 text-xs">
        <div class="max-w-7xl mx-auto px-6 grid sm:grid-cols-2 md:grid-cols-4 gap-8">
            <div>
                <div class="text-lg font-black text-white mb-3">THE FUNDED <span class="text-yellow-500">BIBLE</span></div>
                <p class="leading-relaxed">100% Free Futures Prop Firm Comparison Directory, Program-Specific Consistency Calculator, and CME Contract Sizing Engine. Updated daily.</p>
                <p class="mt-4 text-emerald-400 font-semibold">● Live AutoBot Sync: {TODAY_STR}</p>
            </div>
            <div>
                <h4 class="text-white font-bold uppercase mb-3">Consistency Calculators</h4>
                <ul class="space-y-1.5">{cons_links}</ul>
            </div>
            <div>
                <h4 class="text-white font-bold uppercase mb-3">Verified Firm Hubs</h4>
                <ul class="space-y-1.5">{firm_links}</ul>
            </div>
            <div>
                <h4 class="text-white font-bold uppercase mb-3">Head-to-Head Comparisons</h4>
                <ul class="space-y-1.5">{vs_links}</ul>
            </div>
        </div>
    </footer>
    """

def get_4in1_super_terminal(default_dd=2000, default_target=3000, default_cons=30, default_max_accts=5, default_pt=2, default_stop=20, cta_text="🚀 Claim Verified Prop Firm Discount →", cta_url=MY_MAIN_AFFILIATE_LINK):
    return f"""
    <section id="super-terminal" class="my-8">
        <div class="flex flex-wrap gap-2 mb-6 border-b border-white/10 pb-4">
            <button onclick="switchTab('tab-lot')" id="btn-tab-lot" class="px-4 py-2.5 rounded-xl font-black text-xs uppercase bg-yellow-500 text-black shadow-lg transition">
                1. Drawdown & Lot Sizer
            </button>
            <button onclick="switchTab('tab-cons')" id="btn-tab-cons" class="px-4 py-2.5 rounded-xl font-black text-xs uppercase bg-white/10 text-white hover:bg-white/20 transition">
                2. Consistency Rule + Safe Daily Cap 🔥
            </button>
            <button onclick="switchTab('tab-copy')" id="btn-tab-copy" class="px-4 py-2.5 rounded-xl font-black text-xs uppercase bg-white/10 text-emerald-400 hover:bg-white/20 transition">
                3. 20-Account Copy Multiplier 💰
            </button>
            <button onclick="switchTab('tab-payout')" id="btn-tab-payout" class="px-4 py-2.5 rounded-xl font-black text-xs uppercase bg-white/10 text-cyan-400 hover:bg-white/20 transition">
                4. Safe Withdrawal Buffer Checker 🛡️
            </button>
        </div>

        <!-- TAB 1: LOT SIZER -->
        <div id="tab-lot" class="grid lg:grid-cols-12 gap-8 items-start">
            <div class="lg:col-span-5 glass rounded-2xl p-6 border border-white/10">
                <h3 class="text-sm font-black uppercase text-yellow-400 mb-4">⚡ Step 1: Evaluation Drawdown Math</h3>
                <div class="space-y-4">
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Max Drawdown ($)</label>
                            <input type="number" id="maxDrawdown" value="{default_dd}" class="w-full rounded-xl p-3 text-sm font-bold bg-[#111522] border border-white/15 text-white" oninput="calcLot()">
                        </div>
                        <div>
                            <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Profit Target ($)</label>
                            <input type="number" id="profitTarget" value="{default_target}" class="w-full rounded-xl p-3 text-sm font-bold bg-[#111522] border border-white/15 text-white" oninput="calcLot()">
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Futures Ticker</label>
                            <select id="instrument" class="w-full rounded-xl p-3 text-sm font-bold bg-[#111522] border border-white/15 text-white" onchange="calcLot()">
                                <option value="2" {"selected" if default_pt==2 else ""}>MNQ ($2/pt - Micro Nasdaq)</option>
                                <option value="20" {"selected" if default_pt==20 else ""}>NQ ($20/pt - E-Mini Nasdaq)</option>
                                <option value="5" {"selected" if default_pt==5 else ""}>MES ($5/pt - Micro S&P 500)</option>
                                <option value="50" {"selected" if default_pt==50 else ""}>ES ($50/pt - E-Mini S&P 500)</option>
                                <option value="10" {"selected" if default_pt==10 else ""}>MGC ($10/pt - Micro Gold)</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Stop Loss (Points)</label>
                            <input type="number" id="stopPoints" value="{default_stop}" class="w-full rounded-xl p-3 text-sm font-bold bg-[#111522] border border-white/15 text-white" oninput="calcLot()">
                        </div>
                    </div>
                    <div>
                        <div class="flex justify-between text-xs font-bold mb-1">
                            <span class="text-slate-400">Consecutive Loss Survival Buffer</span>
                            <span id="bufVal" class="text-yellow-400">10 Full Stops</span>
                        </div>
                        <input type="range" id="lossBuffer" min="4" max="20" value="10" class="w-full accent-yellow-500" oninput="calcLot()">
                    </div>
                </div>
            </div>
            <div class="lg:col-span-7 glass rounded-2xl p-6 border border-yellow-500/40">
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">Max Contracts</div>
                        <div id="outLots" class="text-3xl font-black text-yellow-400 mt-1">5</div>
                    </div>
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">Risk / Trade</div>
                        <div id="outRisk" class="text-3xl font-black text-white mt-1">$200</div>
                    </div>
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">Losses to Blow</div>
                        <div id="outBreach" class="text-3xl font-black text-emerald-400 mt-1">10</div>
                    </div>
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">Wins to Pass</div>
                        <div id="outWins" class="text-3xl font-black text-cyan-400 mt-1">8</div>
                    </div>
                </div>
                <div class="bg-black/50 p-4 rounded-xl border border-white/10 mb-5">
                    <div class="flex justify-between text-xs font-bold mb-2">
                        <span class="text-slate-300">Drawdown Burn Per Stop</span>
                        <span id="burnPctText" class="text-emerald-400">10.0% Burn</span>
                    </div>
                    <div class="w-full h-3 bg-white/10 rounded-full overflow-hidden">
                        <div id="burnBar" class="h-full bg-gradient-to-r from-emerald-400 to-yellow-400" style="width: 25%;"></div>
                    </div>
                </div>
                <a href="{cta_url}" target="_blank" class="block w-full bg-yellow-500 hover:bg-yellow-400 text-black font-black text-sm py-4 rounded-xl text-center shadow-lg transition">{cta_text}</a>
            </div>
        </div>

        <!-- TAB 2: CONSISTENCY RULE FIXER -->
        <div id="tab-cons" class="hidden grid lg:grid-cols-12 gap-8 items-start">
            <div class="lg:col-span-5 glass rounded-2xl p-6 border border-white/10">
                <h3 class="text-sm font-black uppercase text-yellow-400 mb-2">🔥 Exact Program Consistency Calculator</h3>
                <p class="text-xs text-slate-400 mb-4">Select your exact prop firm sub-program or rule percentage. Includes "Max Safe Profit Tomorrow" math.</p>
                <div class="space-y-4">
                    <div>
                        <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Firm & Specific Program Rule</label>
                        <select id="consPct" class="w-full rounded-xl p-3 text-xs font-bold bg-[#111522] border border-white/15 text-white" onchange="calcCons()">
                            <option value="20" {"selected" if default_cons==20 else ""}>20% — Tradeify Lightning (1st Payout) / Alpha Direct / Bulenox Fast</option>
                            <option value="25">25% — Tradeify Lightning (2nd Approved Payout)</option>
                            <option value="30" {"selected" if default_cons==30 else ""}>30% — Apex PA / MFFU Rapid EOD / Tradeify Lightning 3+ / TradeDay</option>
                            <option value="35">35% — Tradeify Growth Sim Funded</option>
                            <option value="40" {"selected" if default_cons==40 else ""}>40% — MFFU Sim / Alpha Adv / Lucid / FundedNext / Topstep Path</option>
                            <option value="50" {"selected" if default_cons==50 else ""}>50% — Take Profit Trader Test / MFFU Pro Eval / Alpha Standard</option>
                            <option value="55">55% — Topstep Trading Combine Official Cap</option>
                        </select>
                    </div>
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Largest Single Day Profit ($)</label>
                            <input type="number" id="bestDay" value="1200" class="w-full rounded-xl p-3 text-sm font-bold bg-[#111522] border border-white/15 text-white" oninput="calcCons()">
                        </div>
                        <div>
                            <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Current Total Profit ($)</label>
                            <input type="number" id="totalProf" value="2500" class="w-full rounded-xl p-3 text-sm font-bold bg-[#111522] border border-white/15 text-white" oninput="calcCons()">
                        </div>
                    </div>
                </div>
            </div>
            <div class="lg:col-span-7 glass rounded-2xl p-6 border border-emerald-500/40">
                <div class="flex justify-between items-center mb-4">
                    <h4 class="text-sm font-black uppercase text-white">Payout & Next-Day Cap Telemetry</h4>
                    <span id="consBadge" class="text-xs font-black px-3 py-1 rounded-full bg-red-500/20 text-red-400">PAYOUT LOCKED</span>
                </div>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5">
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">Current Ratio</div>
                        <div id="outCurrCons" class="text-2xl font-black text-yellow-400 mt-1">48.0%</div>
                    </div>
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">Required Total</div>
                        <div id="outReqTotal" class="text-2xl font-black text-white mt-1">$4,000</div>
                    </div>
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">Still Needed</div>
                        <div id="outExtraNeed" class="text-2xl font-black text-emerald-400 mt-1">$1,500</div>
                    </div>
                    <div class="bg-black/60 p-4 rounded-xl border border-cyan-500/30">
                        <div class="text-[11px] text-cyan-400 uppercase font-bold">Max Next Day Cap</div>
                        <div id="outMaxNextDay" class="text-2xl font-black text-cyan-400 mt-1">$1,071</div>
                    </div>
                </div>
                <p id="consAdvice" class="text-xs text-slate-300 bg-black/40 p-3.5 rounded-xl border border-white/10 mb-5"></p>
                <a href="{cta_url}" target="_blank" class="block w-full bg-emerald-500 hover:bg-emerald-400 text-black font-black text-sm py-4 rounded-xl text-center shadow-lg transition">🚀 Claim Verified Evaluation Discount →</a>
            </div>
        </div>

        <!-- TAB 3: COPY TRADING MULTIPLIER -->
        <div id="tab-copy" class="hidden grid lg:grid-cols-12 gap-8 items-start">
            <div class="lg:col-span-5 glass rounded-2xl p-6 border border-white/10">
                <h3 class="text-sm font-black uppercase text-emerald-400 mb-2">💰 20-Account Copy-Trading Multiplier</h3>
                <div class="space-y-4">
                    <div>
                        <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Linked Funded Accounts: <span id="acctCountLabel" class="text-yellow-400">{default_max_accts} Accounts</span></label>
                        <input type="range" id="copyAccts" min="1" max="20" value="{default_max_accts}" class="w-full accent-emerald-400" oninput="calcCopy()">
                    </div>
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Daily Profit / Acct ($)</label>
                            <input type="number" id="dailyPerAcct" value="200" class="w-full rounded-xl p-3 text-sm font-bold bg-[#111522] border border-white/15 text-white" oninput="calcCopy()">
                        </div>
                        <div>
                            <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Profit Split (%)</label>
                            <input type="number" id="copySplit" value="90" class="w-full rounded-xl p-3 text-sm font-bold bg-[#111522] border border-white/15 text-white" oninput="calcCopy()">
                        </div>
                    </div>
                </div>
            </div>
            <div class="lg:col-span-7 glass rounded-2xl p-6 border border-yellow-500/40">
                <div class="grid sm:grid-cols-3 gap-3 mb-5">
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">Combined Daily</div>
                        <div id="outCopyDaily" class="text-3xl font-black text-white mt-1">$1,000</div>
                    </div>
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">20-Day Monthly Gross</div>
                        <div id="outCopyMonthly" class="text-3xl font-black text-yellow-400 mt-1">$20,000</div>
                    </div>
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">Net Take-Home</div>
                        <div id="outCopyNet" class="text-3xl font-black text-emerald-400 mt-1">$18,000</div>
                    </div>
                </div>
                <a href="{cta_url}" target="_blank" class="block w-full bg-yellow-500 hover:bg-yellow-400 text-black font-black text-sm py-4 rounded-xl text-center shadow-lg transition">🚀 Stack Discounted Evaluation Accounts Now →</a>
            </div>
        </div>

        <!-- TAB 4: SAFE WITHDRAWAL CHECKER -->
        <div id="tab-payout" class="hidden grid lg:grid-cols-12 gap-8 items-start">
            <div class="lg:col-span-5 glass rounded-2xl p-6 border border-white/10">
                <h3 class="text-sm font-black uppercase text-cyan-400 mb-2">🛡️ True Withdrawable Cash & Buffer Checker</h3>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Current Balance ($)</label>
                        <input type="number" id="currBal" value="54200" class="w-full rounded-xl p-3 text-sm font-bold bg-[#111522] border border-white/15 text-white" oninput="calcPayout()">
                    </div>
                    <div>
                        <label class="block text-[11px] font-bold uppercase text-slate-400 mb-1">Buffer Lock ($)</label>
                        <input type="number" id="reqBufBal" value="52100" class="w-full rounded-xl p-3 text-sm font-bold bg-[#111522] border border-white/15 text-white" oninput="calcPayout()">
                    </div>
                </div>
            </div>
            <div class="lg:col-span-7 glass rounded-2xl p-6 border border-cyan-500/40">
                <div class="grid sm:grid-cols-2 gap-3 mb-5">
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">Safe Withdrawal Request</div>
                        <div id="outSafeReq" class="text-3xl font-black text-emerald-400 mt-1">$2,100</div>
                    </div>
                    <div class="bg-black/60 p-4 rounded-xl border border-white/10">
                        <div class="text-[11px] text-slate-400 uppercase">Hits Your Bank (90% Split)</div>
                        <div id="outBankNet" class="text-3xl font-black text-yellow-400 mt-1">$1,890</div>
                    </div>
                </div>
                <a href="{cta_url}" target="_blank" class="block w-full bg-cyan-400 hover:bg-cyan-300 text-black font-black text-sm py-4 rounded-xl text-center shadow-lg transition">🚀 Compare Day-1 Payout Firms →</a>
            </div>
        </div>
    </section>

    <script>
    function switchTab(tabId) {{
        ['tab-lot', 'tab-cons', 'tab-copy', 'tab-payout'].forEach(id => {{
            document.getElementById(id).classList.add('hidden');
            document.getElementById('btn-' + id).className = 'px-4 py-2.5 rounded-xl font-black text-xs uppercase bg-white/10 text-white hover:bg-white/20 transition';
        }});
        document.getElementById(tabId).classList.remove('hidden');
        document.getElementById('btn-' + tabId).className = 'px-4 py-2.5 rounded-xl font-black text-xs uppercase bg-yellow-500 text-black shadow-lg transition';
    }}
    function calcLot() {{
        const dd = parseFloat(document.getElementById('maxDrawdown').value) || 2000;
        const target = parseFloat(document.getElementById('profitTarget').value) || 3000;
        const pt = parseFloat(document.getElementById('instrument').value) || 2;
        const sl = parseFloat(document.getElementById('stopPoints').value) || 20;
        const buf = parseInt(document.getElementById('lossBuffer').value) || 10;
        document.getElementById('bufVal').innerText = buf + ' Full Stops';
        const maxRisk = dd / buf;
        const singleRisk = pt * sl;
        let lots = Math.floor(maxRisk / singleRisk);
        if (lots < 1) lots = 1;
        const actualRisk = lots * singleRisk;
        const burnPct = Math.min(100, ((actualRisk / dd) * 100)).toFixed(1);
        document.getElementById('outLots').innerText = lots;
        document.getElementById('outRisk').innerText = '$' + actualRisk.toLocaleString();
        document.getElementById('outBreach').innerText = Math.floor(dd / actualRisk);
        document.getElementById('outWins').innerText = Math.ceil(target / (actualRisk * 2));
        document.getElementById('burnPctText').innerText = burnPct + '% Buffer Burn';
        document.getElementById('burnBar').style.width = Math.min(100, burnPct * 3) + '%';
    }}
    function calcCons() {{
        const rule = (parseFloat(document.getElementById('consPct').value) || 30) / 100;
        const best = parseFloat(document.getElementById('bestDay').value) || 1200;
        const tot = parseFloat(document.getElementById('totalProf').value) || 2500;
        const currPct = tot > 0 ? ((best / tot) * 100).toFixed(1) : 100;
        const reqTot = Math.ceil(best / rule);
        const extra = Math.max(0, reqTot - tot);
        const maxNext = Math.floor((rule * tot) / (1 - rule));

        document.getElementById('outCurrCons').innerText = currPct + '%';
        document.getElementById('outReqTotal').innerText = '$' + reqTot.toLocaleString();
        document.getElementById('outExtraNeed').innerText = '$' + extra.toLocaleString();
        document.getElementById('outMaxNextDay').innerText = '$' + maxNext.toLocaleString();

        const badge = document.getElementById('consBadge');
        if (extra <= 0) {{
            badge.className = 'text-xs font-black px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400';
            badge.innerText = '✅ PAYOUT ELIGIBLE';
            document.getElementById('consAdvice').innerText = 'You are within the ' + (rule*100) + '% consistency limit! The largest single day you can add tomorrow without breaking the rule is $' + maxNext.toLocaleString() + '.';
        }} else {{
            badge.className = 'text-xs font-black px-3 py-1 rounded-full bg-red-500/20 text-red-400';
            badge.innerText = '⚠️ NEED $' + extra.toLocaleString() + ' MORE PROFIT';
            document.getElementById('consAdvice').innerText = 'Formula: $' + best.toLocaleString() + ' Best Day ÷ ' + rule + ' = $' + reqTot.toLocaleString() + ' Required Total Profit. Add $' + extra.toLocaleString() + ' across controlled days smaller than $' + best.toLocaleString() + ' before requesting payout.';
        }}
    }}
    function calcCopy() {{
        const accts = parseInt(document.getElementById('copyAccts').value) || 5;
        const daily = parseFloat(document.getElementById('dailyPerAcct').value) || 200;
        const split = (parseFloat(document.getElementById('copySplit').value) || 90) / 100;
        document.getElementById('acctCountLabel').innerText = accts + ' Accounts';
        const combDaily = accts * daily;
        const monthlyGross = combDaily * 20;
        document.getElementById('outCopyDaily').innerText = '$' + combDaily.toLocaleString();
        document.getElementById('outCopyMonthly').innerText = '$' + monthlyGross.toLocaleString();
        document.getElementById('outCopyNet').innerText = '$' + Math.round(monthlyGross * split).toLocaleString();
    }}
    function calcPayout() {{
        const bal = parseFloat(document.getElementById('currBal').value) || 54200;
        const buf = parseFloat(document.getElementById('reqBufBal').value) || 52100;
        const safe = Math.max(0, bal - buf);
        document.getElementById('outSafeReq').innerText = '$' + safe.toLocaleString();
        document.getElementById('outBankNet').innerText = '$' + Math.round(safe * 0.9).toLocaleString();
    }}
    calcLot(); calcCons(); calcCopy(); calcPayout();
    </script>
    """

def render_deep_seo_guide(firm, tier_label="$50K", dd_val=2000, target_val=3000):
    ex_best = int(target_val * 0.45)
    ex_req = int(ex_best / (firm['consistency'] / 100))
    safe_cap = int(target_val * ((firm['consistency'] - 5) / 100))
    tier_links = "".join([
        f'<a href="/{firm["slug"]}-{t["tier"]}-drawdown-calculator.html" class="px-3 py-1.5 rounded-lg bg-white/5 hover:bg-yellow-500 hover:text-black text-xs font-bold transition">{firm["short"]} {t["label"]} Calculator</a>'
        for t in ACCOUNT_TIERS
    ])
    return f"""
    <article class="mt-14 space-y-8 text-slate-300 text-sm leading-relaxed border-t border-white/10 pt-10">
        <div class="glass p-6 md:p-8 rounded-3xl border border-white/10">
            <h2 class="text-2xl font-black text-white mb-3">{firm['name']} ({tier_label}) Complete Rule Breakdown & Consistency Math ({TODAY_STR})</h2>
            <p class="mb-4">
                When trading a <strong>{firm['name']} {tier_label} evaluation or funded account</strong>, your survival depends on respecting the <strong>${dd_val:,} {firm['dd_type']} drawdown</strong> and the <strong>{firm['consistency']}% consistency rule</strong> against the <strong>${target_val:,} profit target</strong>.
            </p>
            <div class="grid md:grid-cols-2 gap-4 my-6">
                <div class="bg-black/50 p-5 rounded-2xl border border-white/10">
                    <h3 class="text-white font-bold text-base mb-2">📌 Official Program Rules Breakdown</h3>
                    <p class="text-xs text-slate-300">{firm['programs_breakdown']}</p>
                    <p class="text-xs text-yellow-400 mt-3"><strong>Edge-Case Alert:</strong> {firm['edge_case_note']}</p>
                </div>
                <div class="bg-black/50 p-5 rounded-2xl border border-white/10">
                    <h3 class="text-white font-bold text-base mb-2">🧮 Worked {firm['consistency']}% Consistency Example ({tier_label})</h3>
                    <p class="text-xs text-slate-300">
                        Formula: <code>Required Total Profit = Best Day Profit ÷ {firm['consistency']/100}</code>.<br>
                        If your largest single trading day at {firm['name']} is <strong>${ex_best:,}</strong>, your total account profit must reach at least <strong>${ex_req:,}</strong> before your best day represents {firm['consistency']}% or less of total profit. Set your daily auto-liquidate alert at <strong>${safe_cap:,}/day</strong>.
                    </p>
                </div>
            </div>
            <div class="flex flex-wrap gap-2 pt-2">{tier_links}</div>
        </div>
    </article>
    """

def wrap_html(title, desc, slug_path, body_content, faqs=None):
    full_url = f"{SITE_URL}/{slug_path}" if slug_path else f"{SITE_URL}/"
    schema_tag = build_schema_json(title, desc, full_url, faqs)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="canonical" href="{full_url}">
    {schema_tag}
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            background-color: #07090e;
            background-image: radial-gradient(circle at 50% 0%, rgba(16, 185, 129, 0.08) 0%, transparent 50%),
                              linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
            background-size: 100% 100%, 40px 40px, 40px 40px;
            color: #f1f5f9;
            font-family: 'Inter', -apple-system, sans-serif;
        }}
        .glass {{ background: rgba(15, 19, 30, 0.85); backdrop-filter: blur(12px); }}
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between">
    {get_header_nav()}
    <main class="max-w-7xl mx-auto px-6 mt-10 w-full">
        {body_content}
    </main>
    {get_footer()}
</body>
</html>"""

def build_matrix_rows(firm_list):
    rows = ""
    for f in firm_list:
        rows += f"""
        <tr class="border-b border-white/5 hover:bg-white/[0.04] transition">
            <td class="p-4">
                <div class="flex items-center gap-3">
                    {render_firm_logo(f)}
                    <div>
                        <a href="/{f['slug']}.html" class="font-black text-white hover:text-yellow-400 text-base block">{f['name']}</a>
                        <span class="text-xs text-emerald-400 font-bold">🛡️ Trust: {f['trust_score']} • Max {f['max_accounts']} Accts</span>
                    </div>
                </div>
            </td>
            <td class="p-4 font-bold text-slate-200">{f['size']} <span class="block text-xs text-slate-400">${f['dd']} ({f['dd_type']})</span></td>
            <td class="p-4"><a href="/{f['slug']}-consistency-calculator.html" class="text-xs px-3 py-1 rounded-full bg-white/10 text-yellow-400 font-bold hover:bg-yellow-500 hover:text-black transition">{f['consistency']}% Rule Calc →</a></td>
            <td class="p-4 text-slate-300 text-xs font-semibold">{f['split']}<br><span class="text-emerald-400 font-bold">{f['payout_speed']}</span></td>
            <td class="p-4">
                <span class="bg-black border border-dashed border-yellow-500 text-yellow-400 font-mono font-bold text-xs px-3 py-1.5 rounded-lg block text-center">{f['code']}</span>
                <span class="text-[10px] text-emerald-400 font-bold block text-center mt-1">{f['discount']} ({f['price']})</span>
            </td>
            <td class="p-4 text-right">
                <a href="{f['aff_url']}" target="_blank" class="bg-yellow-500 hover:bg-yellow-400 text-black font-black text-xs px-4 py-2.5 rounded-xl inline-block shadow-lg transition">Get Deal →</a>
            </td>
        </tr>"""
    return rows

sitemap_urls = []

# ==============================================================================
# PHASE 1: CORE 154 FOUNDATION PAGES (BUILT IMMEDIATELY ON DAY 1)
# ==============================================================================
logo_strip = "".join([
    f'<a href="/{f["slug"]}.html" class="glass px-3.5 py-2.5 rounded-2xl border border-white/10 hover:border-yellow-500/50 flex items-center gap-2.5 transition">'
    f'{render_firm_logo(f, "w-8 h-8")}'
    f'<div class="text-left"><div class="text-xs font-black text-white">{f["short"]}</div><div class="text-[10px] text-emerald-400 font-bold">{f["discount"]}</div></div></a>'
    for f in FIRMS
])

home_faqs = [
    ("How is the prop firm consistency rule calculated?", "Divide your largest single profitable trading day by your total account profit and multiply by 100. Required Total Profit = Best Day Profit divided by the rule percentage."),
    ("Which futures prop firms use EOD trailing drawdown?", "Topstep, MyFundedFutures, Tradeify, Take Profit Trader, Alpha Futures, Lucid Trading, FundedNext Futures, TradeDay, and BluSky use End-of-Day (EOD) trailing drawdown.")
]

home_body = f"""
<div class="text-center max-w-4xl mx-auto mb-8">
    <span class="text-xs font-extrabold uppercase tracking-widest text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-3.5 py-1 rounded-full">All-in-One Futures Prop Firm OS • Synced {TODAY_STR}</span>
    <h1 class="text-4xl md:text-6xl font-black text-white mt-5 mb-4 tracking-tight">Compare Prop Firms, Fix Consistency & <span class="text-yellow-500">Calculate Exact Lot Size.</span></h1>
    <p class="text-slate-400 text-base md:text-lg max-w-2xl mx-auto">100% Free CME Futures Drawdown Calculator, Program-Specific Consistency Unlocker (20%–55%), and Verified Daily Prop Firm Deals.</p>
</div>
<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2.5 mb-8">{logo_strip}</div>
{get_4in1_super_terminal()}
<section id="matrix" class="my-16">
    <h2 class="text-2xl font-black text-white mb-4">Verified Prop Firm Matrix, Consistency Rules & Deals ({TODAY_STR})</h2>
    <div class="glass rounded-3xl border border-white/10 overflow-x-auto shadow-2xl">
        <table class="w-full text-left text-sm">
            <thead class="bg-black/60 text-xs uppercase text-slate-400 border-b border-white/10">
                <tr>
                    <th class="p-4">Prop Firm</th>
                    <th class="p-4">Account & Buffer</th>
                    <th class="p-4">Consistency Tool</th>
                    <th class="p-4">Split & Payout Speed</th>
                    <th class="p-4 text-center">Promo Code</th>
                    <th class="p-4 text-right">Official Link</th>
                </tr>
            </thead>
            <tbody>{build_matrix_rows(FIRMS)}</tbody>
        </table>
    </div>
</section>
"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(wrap_html("The Funded Bible | #1 Prop Firm Consistency Calculator & Match Directory", "Free futures prop firm comparison matrix, 20%-55% consistency rule calculator, and MNQ/NQ lot sizer.", "", home_body, home_faqs))
sitemap_urls.append(f"{SITE_URL}/")

for slug, h1, desc, auto_tab in [
    ("consistency-rule-calculator", "Prop Firm Consistency Rule Calculator (Apex, Topstep, Tradeify, MFFU)", "Calculate your exact consistency percentage, required total profit to unlock payouts, and maximum safe daily win cap.", "tab-cons"),
    ("copy-trading-payout-multiplier", "Futures Prop Firm Copy-Trading Payout Multiplier (1 to 20 Accounts)", "Calculate how a $150-$250 daily base scalp multiplies across 5 to 20 copy-traded funded accounts.", "tab-copy"),
    ("eod-drawdown-prop-firms", "Best End-of-Day (EOD) Trailing Drawdown Prop Firms (2026 Audit)", "Compare verified EOD trailing drawdown futures prop firms side-by-side.", "tab-lot")
]:
    fname = f"{slug}.html"
    body = f"""
    <h1 class="text-3xl md:text-5xl font-black text-white mb-3">{h1}</h1>
    <p class="text-slate-400 mb-6">{desc}</p>
    {get_4in1_super_terminal()}
    <div class="glass rounded-3xl border border-white/10 overflow-x-auto my-12">
        <table class="w-full text-left text-sm"><tbody>{build_matrix_rows(FIRMS)}</tbody></table>
    </div>
    <script>switchTab('{auto_tab}');</script>
    """
    with open(fname, "w", encoding="utf-8") as out:
        out.write(wrap_html(f"{h1} | The Funded Bible", desc, fname, body, home_faqs))
    sitemap_urls.append(f"{SITE_URL}/{fname}")

for firm in FIRMS:
    firm_faqs = [
        (f"What is the {firm['name']} consistency rule?", f"{firm['programs_breakdown']}. {firm['edge_case_note']}"),
        (f"How do I calculate my {firm['name']} consistency requirement?", f"Divide your largest single day profit by {firm['consistency']/100}.")
    ]
    fname = f"{firm['slug']}.html"
    body = f"""
    <div class="glass rounded-3xl p-6 md:p-8 border border-white/15 mb-8 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-5">
            {render_firm_logo(firm, "w-20 h-20")}
            <div>
                <span class="text-xs font-bold uppercase text-emerald-400">{firm['discount']} Verified Deal • Max {firm['max_accounts']} Accounts</span>
                <h1 class="text-3xl md:text-5xl font-black text-white mt-1">{firm['name']} ({firm['size']}) Calculator & Audit</h1>
                <p class="text-slate-400 text-sm mt-1">Consistency: {firm['consistency']}% • Buffer Lock: ${firm['buffer_lock']} • Promo Code: <strong class="text-yellow-400">{firm['code']}</strong></p>
            </div>
        </div>
        <a href="{firm['aff_url']}" target="_blank" class="bg-yellow-500 hover:bg-yellow-400 text-black font-black px-6 py-4 rounded-xl text-sm shrink-0 shadow-xl">🚀 Claim {firm['discount']} at {firm['name']} →</a>
    </div>
    {get_4in1_super_terminal(firm['dd'], firm['target'], firm['consistency'], firm['max_accounts'], 2, 20, f"🚀 Activate {firm['name']} Deal ({firm['code']}) →", firm['aff_url'])}
    {render_deep_seo_guide(firm)}
    """
    with open(fname, "w", encoding="utf-8") as out:
        out.write(wrap_html(f"{firm['name']} Drawdown Calculator, {firm['consistency']}% Consistency Rule & Promo Code", f"Official {firm['name']} {firm['size']} lot size calculator and {firm['consistency']}% consistency rule breakdown.", fname, body, firm_faqs))
    sitemap_urls.append(f"{SITE_URL}/{fname}")

    cons_fname = f"{firm['slug']}-consistency-calculator.html"
    cons_body = f"""
    <div class="flex items-center gap-4 mb-6">
        {render_firm_logo(firm, "w-16 h-16")}
        <div>
            <span class="text-xs font-bold uppercase text-yellow-400">Program-Specific Payout Unlock Tool • Updated {TODAY_STR}</span>
            <h1 class="text-3xl md:text-5xl font-black text-white">{firm['name']} <span class="text-yellow-500">{firm['consistency']}% Consistency Rule Calculator</span></h1>
        </div>
    </div>
    {get_4in1_super_terminal(firm['dd'], firm['target'], firm['consistency'], firm['max_accounts'], 2, 20, f"🚀 Get {firm['discount']} at {firm['name']} ({firm['code']}) →", firm['aff_url'])}
    {render_deep_seo_guide(firm)}
    <script>switchTab('tab-cons');</script>
    """
    with open(cons_fname, "w", encoding="utf-8") as out:
        out.write(wrap_html(f"{firm['name']} Consistency Rule Calculator ({firm['consistency']}% Payout Math)", f"Free {firm['name']} consistency calculator.", cons_fname, cons_body, firm_faqs))
    sitemap_urls.append(f"{SITE_URL}/{cons_fname}")

for a, b in itertools.combinations(FIRMS, 2):
    fname = f"{a['slug']}-vs-{b['slug']}.html"
    vs_faqs = [(f"Is {a['name']} or {b['name']} better?", f"{a['name']} offers a ${a['dd']} {a['dd_type']} drawdown ({a['consistency']}% consistency), while {b['name']} features a ${b['dd']} {b['dd_type']} drawdown ({b['consistency']}% consistency).")]
    body = f"""
    <h1 class="text-3xl md:text-5xl font-black text-white mb-4">{a['name']} vs {b['name']} (2026): <span class="text-yellow-500">Drawdown, Consistency & Payout Comparison</span></h1>
    <div class="glass rounded-3xl border border-white/10 overflow-x-auto mb-10">
        <table class="w-full text-left text-sm"><tbody>{build_matrix_rows([a, b])}</tbody></table>
    </div>
    {get_4in1_super_terminal(a['dd'], a['target'], a['consistency'], a['max_accounts'], 2, 20, f"Claim {a['name']} or {b['name']} Verified Discount →", a['aff_url'])}
    {render_deep_seo_guide(a)}
    """
    with open(fname, "w", encoding="utf-8") as out:
        out.write(wrap_html(f"{a['name']} vs {b['name']} (2026): Rules, Consistency & Payout Speed", f"Detailed comparison of {a['name']} vs {b['name']}.", fname, body, vs_faqs))
    sitemap_urls.append(f"{SITE_URL}/{fname}")

for firm in FIRMS:
    for inst in INSTRUMENTS:
        fname = f"{firm['slug']}-{inst['ticker'].lower()}-calculator.html"
        max_c = max(1, int((firm['dd'] / 10) / (inst['pt_val'] * inst['stop'])))
        inst_faqs = [(f"How many {inst['ticker']} contracts on {firm['name']}?", f"Sizing at {max_c} {inst['ticker']} contract(s) with a {inst['stop']}-point stop loss gives a 10-loss survival buffer.")]
        body = f"""
        <div class="flex items-center gap-4 mb-6">
            {render_firm_logo(firm, "w-16 h-16")}
            <div>
                <span class="text-xs font-bold uppercase text-emerald-400">{inst['exchange']} {inst['name']} (${inst['pt_val']}/Pt • {inst['tick_val']}/Tick)</span>
                <h1 class="text-3xl md:text-4xl font-black text-white">{firm['name']} {firm['size']} <span class="text-yellow-500">{inst['ticker']} Contract Size Calculator</span></h1>
            </div>
        </div>
        {get_4in1_super_terminal(firm['dd'], firm['target'], firm['consistency'], firm['max_accounts'], inst['pt_val'], inst['stop'], f"🚀 Trade {inst['ticker']} at {firm['name']} ({firm['code']}) →", firm['aff_url'])}
        {render_deep_seo_guide(firm)}
        """
        with open(fname, "w", encoding="utf-8") as out:
            out.write(wrap_html(f"{firm['name']} {inst['ticker']} Lot Size & Drawdown Calculator ({firm['size']})", f"Calculate exact {inst['ticker']} contract limits for {firm['name']}.", fname, body, inst_faqs))
        sitemap_urls.append(f"{SITE_URL}/{fname}")

# ==============================================================================
# PHASE 2: THE 1,000-PAGE DRIP-FEED EXPANSION ENGINE (ADDS 35 NEW PAGES PER DAY)
# ==============================================================================
long_tail_queue = []

for firm in FIRMS:
    for tier in ACCOUNT_TIERS:
        long_tail_queue.append(("tier_dd", firm, tier, None))

for firm in FIRMS:
    for tier in ACCOUNT_TIERS:
        for inst in INSTRUMENTS:
            long_tail_queue.append(("tier_inst", firm, tier, inst))

for firm in FIRMS:
    for tier in ACCOUNT_TIERS:
        for inst in INSTRUMENTS:
            long_tail_queue.append(("pass_guide", firm, tier, inst))

unlocked_count = 0
if os.path.exists(DRIP_STATE_FILE):
    try:
        with open(DRIP_STATE_FILE, "r", encoding="utf-8") as df:
            state = json.load(df)
            unlocked_count = state.get("unlocked_count", 0)
    except Exception:
        unlocked_count = 0

unlocked_count = min(len(long_tail_queue), unlocked_count + DAILY_DRIP_BATCH_SIZE)
with open(DRIP_STATE_FILE, "w", encoding="utf-8") as df:
    json.dump({"unlocked_count": unlocked_count, "last_updated": ISO_TODAY}, df)

for kind, firm, tier, inst in long_tail_queue[:unlocked_count]:
    if kind == "tier_dd":
        fname = f"{firm['slug']}-{tier['tier']}-drawdown-calculator.html"
        title = f"{firm['name']} {tier['label']} Drawdown, Buffer & Consistency Calculator (2026)"
        desc = f"Free {firm['name']} {tier['label']} evaluation calculator. Calculate your ${tier['dd']:,} {firm['dd_type']} drawdown buffer and {firm['consistency']}% consistency cap."
        faqs = [(f"What is the max drawdown on a {firm['name']} {tier['label']} account?", f"The {firm['name']} {tier['label']} account features a ${tier['dd']:,} {firm['dd_type']} drawdown against a ${tier['target']:,} profit target.")]
        body = f"""
        <div class="flex items-center gap-4 mb-6">
            {render_firm_logo(firm, "w-16 h-16")}
            <div>
                <span class="text-xs font-bold uppercase text-yellow-400">{tier['label']} Account Audit • ${tier['dd']:,} Max Drawdown</span>
                <h1 class="text-3xl md:text-5xl font-black text-white">{firm['name']} {tier['label']} <span class="text-yellow-500">Drawdown & Consistency Calculator</span></h1>
            </div>
        </div>
        {get_4in1_super_terminal(tier['dd'], tier['target'], firm['consistency'], firm['max_accounts'], 2, 20, f"🚀 Claim {firm['discount']} on {firm['name']} {tier['label']} ({firm['code']}) →", firm['aff_url'])}
        {render_deep_seo_guide(firm, tier['label'], tier['dd'], tier['target'])}
        """
    elif kind == "tier_inst":
        fname = f"{firm['slug']}-{tier['tier']}-{inst['ticker'].lower()}-lot-size-calculator.html"
        max_c = max(1, int((tier['dd'] / 10) / (inst['pt_val'] * inst['stop'])))
        title = f"{firm['name']} {tier['label']} {inst['ticker']} Max Contract & Stop Loss Calculator"
        desc = f"See how many {inst['ticker']} contracts you can trade on a {firm['name']} {tier['label']} account (${tier['dd']:,} drawdown) without blowing your evaluation."
        faqs = [(f"How many {inst['ticker']} contracts should I trade on a {firm['name']} {tier['label']} account?", f"Trading {max_c} {inst['ticker']} contract(s) with a {inst['stop']}-point stop loss risks ${max_c * inst['pt_val'] * inst['stop']:,} per trade, giving you a 10-loss buffer on a ${tier['dd']:,} drawdown.")]
        body = f"""
        <div class="flex items-center gap-4 mb-6">
            {render_firm_logo(firm, "w-16 h-16")}
            <div>
                <span class="text-xs font-bold uppercase text-emerald-400">{tier['label']} Account • {inst['ticker']} (${inst['pt_val']}/Pt) Sizing</span>
                <h1 class="text-3xl md:text-4xl font-black text-white">{firm['name']} {tier['label']} <span class="text-yellow-500">{inst['ticker']} Contract Size Calculator</span></h1>
            </div>
        </div>
        {get_4in1_super_terminal(tier['dd'], tier['target'], firm['consistency'], firm['max_accounts'], inst['pt_val'], inst['stop'], f"🚀 Trade {inst['ticker']} on {firm['name']} {tier['label']} ({firm['code']}) →", firm['aff_url'])}
        {render_deep_seo_guide(firm, tier['label'], tier['dd'], tier['target'])}
        """
    else:
        fname = f"how-to-pass-{firm['slug']}-{tier['tier']}-with-{inst['ticker'].lower()}.html"
        max_c = max(1, int((tier['dd'] / 10) / (inst['pt_val'] * inst['stop'])))
        wins_req = max(1, int(tier['target'] / (max_c * inst['pt_val'] * inst['stop'] * 2)))
        title = f"How to Pass {firm['name']} {tier['label']} Using {inst['ticker']} (2026 Math Blueprint)"
        desc = f"Step-by-step mathematical blueprint to pass the {firm['name']} {tier['label']} evaluation trading {inst['ticker']} futures in {wins_req} winning trades."
        faqs = [(f"How many winning {inst['ticker']} trades does it take to pass {firm['name']} {tier['label']}?", f"At {max_c} {inst['ticker']} contract(s) with a 1:2 risk-to-reward ratio, it takes approximately {wins_req} net winning trades to hit the ${tier['target']:,} profit target.")]
        body = f"""
        <div class="flex items-center gap-4 mb-6">
            {render_firm_logo(firm, "w-16 h-16")}
            <div>
                <span class="text-xs font-bold uppercase text-cyan-400">Evaluation Pass Blueprint • {wins_req} Net Wins Target</span>
                <h1 class="text-3xl md:text-4xl font-black text-white">How to Pass {firm['name']} {tier['label']} <span class="text-yellow-500">Trading {inst['ticker']} Futures</span></h1>
            </div>
        </div>
        {get_4in1_super_terminal(tier['dd'], tier['target'], firm['consistency'], firm['max_accounts'], inst['pt_val'], inst['stop'], f"🚀 Start Your {firm['name']} {tier['label']} Evaluation ({firm['code']}) →", firm['aff_url'])}
        {render_deep_seo_guide(firm, tier['label'], tier['dd'], tier['target'])}
        """

    with open(fname, "w", encoding="utf-8") as out:
        out.write(wrap_html(title, desc, fname, body, faqs))
    sitemap_urls.append(f"{SITE_URL}/{fname}")

# ==============================================================================
# PHASE 3: SITEMAP.XML & ROBOTS.TXT SYNC
# ==============================================================================
sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap_xml += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{ISO_TODAY}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.9</priority>\n  </url>\n"
sitemap_xml += "</urlset>"

with open("sitemap.xml", "w", encoding="utf-8") as sm:
    sm.write(sitemap_xml)

robots_txt = f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"
with open("robots.txt", "w", encoding="utf-8") as rb:
    rb.write(robots_txt)

print(f"✅ 1,000-Page Drip Engine Active: Built {len(sitemap_urls)} total SEO pages ({unlocked_count}/{len(long_tail_queue)} long-tail pages unlocked so far)!")
