import os
from datetime import datetime

# Prop Firm Database Matrix
prop_firms = [
    {"id": "topstep", "name": "Topstep", "code": "BIBLE", "url": "https://topstep.com/?coupon=BIBLE", "drawdown": "End of Day (EOD)", "consistency": "50% Rule", "split": "90/10", "fee": "$149"},
    {"id": "tradeify", "name": "Tradeify", "code": "BIBLE", "url": "https://tradeify.co/?ref=BIBLE", "drawdown": "Trailing Intraday", "consistency": "No Consistency Rule", "split": "90/10", "fee": "$0"},
    {"id": "mffu", "name": "MyFundedFutures", "code": "BIBLE", "url": "https://myfundedfutures.com/?ref=BIBLE", "drawdown": "EOD / Static", "consistency": "None on Starter", "split": "90/10", "fee": "$0"},
    {"id": "takeprofittrader", "name": "Take Profit Trader", "code": "BIBLE", "url": "https://takeprofittrader.com/?coupon=BIBLE", "drawdown": "Intraday Peak", "consistency": "50% Rule", "split": "80/20 - 90/10", "fee": "$130"},
    {"id": "apex", "name": "Apex Trader Funding", "code": "BIBLE80", "url": "https://apextraderfunding.com/?ref=BIBLE", "drawdown": "Unrealized Trailing", "consistency": "30% on PA", "split": "90/10", "fee": "$85/mo"},
    {"id": "bulenox", "name": "Bulenox", "code": "BIBLE", "url": "https://bulenox.com/?ref=BIBLE", "drawdown": "EOD Trailing", "consistency": "40% Rule", "split": "90/10", "fee": "$0"},
    {"id": "fundednext", "name": "FundedNext Futures", "code": "BIBLE", "url": "https://fundednext.com/?ref=BIBLE", "drawdown": "Balance-Based", "consistency": "None", "split": "90/10", "fee": "$0"},
    {"id": "tradeday", "name": "TradeDay", "code": "BIBLE", "url": "https://tradeday.com/?ref=BIBLE", "drawdown": "End of Day", "consistency": "None", "split": "90/10", "fee": "$0"}
]

account_sizes = ["25k", "50k", "100k", "150k", "250k", "300k"]
us_states = ["texas", "california", "florida", "new-york", "illinois", "ohio", "georgia", "north-carolina", "pennsylvania", "michigan"]

generated_urls = ["https://thefundedbible.com/"]

def build_page(title, description, body_content, canonical_url):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | The Funded Bible</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical_url}">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans">
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur p-4 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto flex justify-between items-center">
      <a href="/" class="text-xl font-black tracking-wider text-amber-400">THE FUNDED BIBLE</a>
      <nav class="space-x-4 text-sm font-semibold">
        <a href="/#matrix" class="hover:text-amber-400">Firm Matrix</a>
        <a href="/#rules" class="hover:text-amber-400">Rules Guide</a>
        <a href="/#discounts" class="hover:text-amber-400">Promo Codes</a>
      </nav>
    </div>
  </header>

  <main class="max-w-4xl mx-auto px-4 py-12 flex-grow">
    {body_content}
  </main>

  <div class="fixed bottom-0 left-0 right-0 bg-slate-900 border-t border-amber-500/40 p-4 shadow-2xl z-40">
    <div class="max-w-4xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
      <div>
        <p class="text-sm font-bold text-amber-400 uppercase tracking-wide">Stop Blowing Evaluations</p>
        <p class="text-xs text-slate-300">Automated Risk & Consistency Calculator (Google Sheet)</p>
      </div>
      <a href="https://buy.stripe.com/YOUR_STRIPE_PAYMENT_LINK" class="bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold px-5 py-2.5 rounded text-sm transition">Get Access ($39)</a>
    </div>
  </div>

  <footer class="border-t border-slate-900 bg-slate-950 py-8 text-center text-xs text-slate-500 mb-16">
    © {datetime.now().year} The Funded Bible LLC. Futures trading involves substantial risk of loss.
  </footer>
</body>
</html>"""

# Matrix 1: Head-to-Head Comparisons
for i in range(len(prop_firms)):
    for j in range(i + 1, len(prop_firms)):
        f1, f2 = prop_firms[i], prop_firms[j]
        slug = f"{f1['id']}-vs-{f2['id']}"
        page_url = f"https://thefundedbible.com/{slug}.html"
        generated_urls.append(page_url)

        title = f"{f1['name']} vs {f2['name']} (2026 Comparison) - Rules, Drawdown & Payouts"
        desc = f"Compare {f1['name']} against {f2['name']}. Review drawdown types, consistency rules, and promo codes."

        content = f"""
        <h1 class="text-3xl sm:text-4xl font-black mb-4">{f1['name']} vs {f2['name']}</h1>
        <p class="text-slate-400 mb-8 text-lg">Detailed rules, drawdown systems, and active discounts for both firms.</p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <h2 class="text-2xl font-bold text-amber-400 mb-2">{f1['name']}</h2>
            <ul class="text-sm space-y-2 mb-6 text-slate-300">
              <li>• Drawdown: <strong>{f1['drawdown']}</strong></li>
              <li>• Consistency: {f1['consistency']}</li>
              <li>• Profit Split: {f1['split']}</li>
              <li>• Activation Fee: {f1['fee']}</li>
            </ul>
            <a href="{f1['url']}" target="_blank" class="block text-center bg-blue-600 hover:bg-blue-500 font-bold py-2.5 rounded text-white transition">Visit {f1['name']} (Code: {f1['code']})</a>
          </div>
          <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <h2 class="text-2xl font-bold text-amber-400 mb-2">{f2['name']}</h2>
            <ul class="text-sm space-y-2 mb-6 text-slate-300">
              <li>• Drawdown: <strong>{f2['drawdown']}</strong></li>
              <li>• Consistency: {f2['consistency']}</li>
              <li>• Profit Split: {f2['split']}</li>
              <li>• Activation Fee: {f2['fee']}</li>
            </ul>
            <a href="{f2['url']}" target="_blank" class="block text-center bg-blue-600 hover:bg-blue-500 font-bold py-2.5 rounded text-white transition">Visit {f2['name']} (Code: {f2['code']})</a>
          </div>
        </div>
        """
        with open(f"{slug}.html", "w", encoding="utf-8") as f:
            f.write(build_page(title, desc, content, page_url))

# Matrix 2: Account Sizes & Targets
for firm in prop_firms:
    for size in account_sizes:
        slug = f"{firm['id']}-{size}-account-rules"
        page_url = f"https://thefundedbible.com/{slug}.html"
        generated_urls.append(page_url)

        title = f"{firm['name']} ${size.upper()} Account Rules & Drawdown"
        desc = f"Complete evaluation guide for {firm['name']} {size.upper()} accounts. Payout terms and rules explained."

        content = f"""
        <h1 class="text-3xl font-black mb-4">{firm['name']} ${size.upper()} Account Guide</h1>
        <div class="bg-slate-900 p-6 rounded-lg border border-slate-800 mb-6">
          <p class="mb-2"><strong>Drawdown Type:</strong> {firm['drawdown']}</p>
          <p class="mb-2"><strong>Consistency Target:</strong> {firm['consistency']}</p>
          <p class="mb-4"><strong>Profit Split:</strong> {firm['split']}</p>
          <a href="{firm['url']}" target="_blank" class="inline-block bg-amber-500 text-slate-950 px-6 py-2.5 rounded font-bold">Get {firm['name']} {size.upper()} (Code: {firm['code']})</a>
        </div>
        """
        with open(f"{slug}.html", "w", encoding="utf-8") as f:
            f.write(build_page(title, desc, content, page_url))

# Matrix 3: State Eligibility
for firm in prop_firms:
    for state in us_states:
        state_name = state.replace("-", " ").title()
        slug = f"can-you-trade-{firm['id']}-in-{state}"
        page_url = f"https://thefundedbible.com/{slug}.html"
        generated_urls.append(page_url)

        title = f"Can You Trade {firm['name']} in {state_name}? (2026 Rules)"
        desc = f"Is {firm['name']} permitted for traders located in {state_name}? Complete eligibility and payout guide."

        content = f"""
        <h1 class="text-3xl font-black mb-4">Trading {firm['name']} from {state_name}</h1>
        <div class="bg-slate-900 p-6 rounded-lg border border-slate-800">
          <p class="text-slate-300 mb-4">Yes, traders in {state_name} can trade simulated evaluation accounts with {firm['name']}.</p>
          <a href="{firm['url']}" target="_blank" class="bg-blue-600 text-white px-6 py-2.5 rounded font-bold">Start Trading with {firm['name']}</a>
        </div>
        """
        with open(f"{slug}.html", "w", encoding="utf-8") as f:
            f.write(build_page(title, desc, content, page_url))

# Build Google-Compliant Sitemap
sitemap_entries = "\n".join([f"  <url><loc>{u}</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod><priority>0.8</priority></url>" for u in generated_urls])
sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_entries}
</urlset>"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

print(f"Generated {len(generated_urls)} pages and sitemap.xml successfully.")
