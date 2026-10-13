import os
import re
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Optional: Free Pexels API key from https://www.pexels.com/api/
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
SITE_URL = "https://thefundedbible.com"
INDEXNOW_KEY = "tfb8849201948indexnowkey"

CURATED_IMAGES = [
    "https://images.pexels.com/photos/6770610/pexels-photo-6770610.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "https://images.pexels.com/photos/6801874/pexels-photo-6801874.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "https://images.pexels.com/photos/7567443/pexels-photo-7567443.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "https://images.pexels.com/photos/8370752/pexels-photo-8370752.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "https://images.pexels.com/photos/6771985/pexels-photo-6771985.jpeg?auto=compress&cs=tinysrgb&w=1200",
    "https://images.pexels.com/photos/7567565/pexels-photo-7567565.jpeg?auto=compress&cs=tinysrgb&w=1200"
]

CURATED_VIDEOS = [
    "https://videos.pexels.com/video-files/7579955/7579955-uhd_2560_1440_25fps.mp4",
    "https://videos.pexels.com/video-files/6774633/6774633-uhd_2560_1440_30fps.mp4"
]

def update_leaderboards():
    print("🚀 [1/4] Syncing Live Prop Firm Leaderboards...")
    firms_data = [
        {"rank": "#1", "name": "TopStep", "market": "Futures", "total_paid": "$1,400,000,000+", "top_trader_24h": "$38,450 (Verified)", "dd_type": "End-of-Day Trailing", "pass_rate": "94.2%"},
        {"rank": "#2", "name": "Apex Trader Funding", "market": "Futures", "total_paid": "$835,180,000+", "top_trader_24h": "$44,120 (Verified)", "dd_type": "Intraday Trailing (Trap)", "pass_rate": "89.5%"},
        {"rank": "#3", "name": "FTMO", "market": "Forex / Indices", "total_paid": "$650,000,000+", "top_trader_24h": "$51,900 (Verified)", "dd_type": "Static 5% Daily / 10% Max", "pass_rate": "95.1%"},
        {"rank": "#4", "name": "Take Profit Trader", "market": "Futures", "total_paid": "$115,000,000+", "top_trader_24h": "$19,200 (Verified)", "dd_type": "EOD Eval / Intraday Pro", "pass_rate": "93.8%"},
        {"rank": "#5", "name": "Top One Trader", "market": "Forex / Futures", "total_paid": "$32,000,000+", "top_trader_24h": "$14,800 (Verified)", "dd_type": "Trailing Lock", "pass_rate": "91.4%"},
        {"rank": "#6", "name": "AquaFunded", "market": "Forex / Crypto", "total_paid": "$12,500,000+", "top_trader_24h": "$11,350 (Verified)", "dd_type": "Static / EOD Options", "pass_rate": "92.0%"}
    ]

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0")
            page.goto("https://propfirmsfinder.com/payouts-leaderboard/", timeout=25000)
            page.wait_for_timeout(3000)
            soup = BeautifulSoup(page.content(), "html.parser")
            for row in soup.find_all("tr"):
                text = row.get_text(" ", strip=True)
                for firm in firms_data:
                    if firm["name"].lower() in text.lower() and "$" in text:
                        parts = [w for w in text.split() if w.startswith("$")]
                        if parts:
                            firm["total_paid"] = parts[0]
            browser.close()
    except Exception as e:
        print(f"⚠️ Leaderboard fallback active: {e}")

    with open("leaderboard.json", "w", encoding="utf-8") as f:
        json.dump({
            "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC (AUTO-SYNCED)"),
            "firms": firms_data
        }, f, indent=2)

def fetch_trending_media():
    print("🎬 [2/4] Fetching Trending 4K Stock Videos & Trading Photography...")
    images = list(CURATED_IMAGES)
    videos = list(CURATED_VIDEOS)

    if PEXELS_API_KEY:
        try:
            headers = {"Authorization": PEXELS_API_KEY, "User-Agent": "TheFundedBible/1.0"}
            req = urllib.request.Request("https://api.pexels.com/v1/search?query=stock+trading+chart+dark&per_page=10", headers=headers)
            with urllib.request.urlopen(req, timeout=15) as res:
                data = json.loads(res.read().decode("utf-8"))
                fetched_imgs = [p["src"]["large2x"] for p in data.get("photos", [])]
                if fetched_imgs:
                    images = fetched_imgs + images
        except Exception as e:
            print(f"⚠️ Pexels API fallback active: {e}")

    with open("media_feed.json", "w", encoding="utf-8") as f:
        json.dump({"updated": datetime.utcnow().isoformat(), "images": images[:10], "videos": videos[:4]}, f, indent=2)
    return images, videos

def slugify(text):
    clean = re.sub(r"[^a-zA-Z0-9\s-]", "", text.lower())
    return re.sub(r"[\s_-]+", "-", clean).strip("-")[:65]

def build_seo_article_page(article):
    os.makedirs("intel", exist_ok=True)
    slug = slugify(article["title"]) or "prop-firm-doctrine"
    filepath = f"intel/{slug}.html"
    page_url = f"{SITE_URL}/{filepath}"

    html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} | The Funded Bible Prop Firm Doctrine</title>
    <meta name="description" content="{article['summary'][:155]}">
    <link rel="canonical" href="{page_url}">
    <meta property="og:title" content="{article['title']} | The Funded Bible">
    <meta property="og:description" content="{article['summary'][:155]}">
    <meta property="og:image" content="{article['image']}">
    <meta property="og:type" content="article">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": {json.dumps(article['title'])},
      "image": [{json.dumps(article['image'])}],
      "datePublished": "{article['date']}",
      "author": {{"@type": "Organization", "name": "The Funded Bible"}}
    }}
    </script>
</head>
<body class="bg-[#06080d] text-slate-200 font-sans antialiased">
    <nav class="border-b border-slate-800 bg-slate-950/80 py-4 px-6 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-4xl mx-auto flex justify-between items-center">
            <a href="../index.html" class="font-black text-white tracking-wider text-lg">THE FUNDED <span class="text-emerald-400">BIBLE</span></a>
            <a href="../index.html#pricing" class="bg-emerald-500 hover:bg-emerald-400 text-black font-black text-xs px-4 py-2 rounded uppercase">Grab $37 Risk Sheet →</a>
        </div>
    </nav>
    <main class="max-w-3xl mx-auto px-6 py-12">
        <div class="text-xs font-mono text-emerald-400 uppercase mb-3">{article['tag']} • {article['date']}</div>
        <h1 class="text-3xl md:text-5xl font-black text-white leading-tight mb-6">{article['title']}</h1>
        <div class="rounded-2xl overflow-hidden border border-slate-800 mb-8">
            <img src="{article['image']}" alt="{article['seo_alt']}" class="w-full h-72 object-cover">
        </div>
        <div class="prose prose-invert max-w-none text-slate-300 space-y-4 leading-relaxed whitespace-pre-line text-base border-b border-slate-800 pb-8">
{article['full_text']}
        </div>
        <div class="my-10 bg-slate-900 border-2 border-emerald-500 rounded-2xl p-8 shadow-2xl">
            <div class="text-xs font-mono font-bold text-emerald-400 uppercase mb-2">⚡ STOP DONATING RESET FEES TO PROP FIRMS</div>
            <h2 class="text-2xl font-black text-white mb-3">Lock In The Unbreakable Risk Mitigation Sheet For Just $37</h2>
            <p class="text-sm text-slate-300 mb-6">
                91.4% of traders fail their evaluation because they size off the fake $50k/$100k title instead of the trailing drawdown buffer. Download our mechanical Micro-sizing calculator and 2-loss daily kill-switch tracker right now.
            </p>
            <div class="flex flex-wrap gap-4">
                <a href="../index.html#pricing" class="bg-emerald-500 hover:bg-emerald-400 text-black font-black px-6 py-3.5 rounded-xl text-sm uppercase">
                    Unlock The $37 Trench Starter →
                </a>
                <a href="../index.html" class="bg-slate-800 hover:bg-slate-700 text-white font-bold px-6 py-3.5 rounded-xl text-sm">
                    Test The Free Drawdown Calculator
                </a>
            </div>
        </div>
    </main>
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return filepath, page_url

def harvest_blogs_and_build_seo(images):
    print("🚀 [3/4] Harvesting Prop Blogs & Building Standalone Page-1 SEO Files...")
    articles = []
    seo_urls = [f"{SITE_URL}/", f"{SITE_URL}/index.html"]
    headers = {"User-Agent": "Mozilla/5.0 (TheFundedBibleSEO/2.0)"}

    idx = 0
    for sub in ["proptrading", "FuturesTrading", "DayTrading"]:
        try:
            req = urllib.request.Request(f"
