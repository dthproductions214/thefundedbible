import os
import re
import json
import urllib.request
import urllib.parse

HOST = "thefundedbible.com"
DOMAIN = f"https://{HOST}"
INDEXNOW_KEY = "tfb2026indexnowkey8899dthpropbots"
KEY_LOCATION = f"{DOMAIN}/{INDEXNOW_KEY}.txt"

# Extract every live URL from sitemap.xml
urls = []
if os.path.exists("sitemap.xml"):
    with open("sitemap.xml", "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    urls = re.findall(r"<loc>(.*?)</loc>", content)

if not urls:
    print("No URLs found in sitemap.xml! Scanning local HTML files...")
    for root, dirs, files in os.walk("."):
        if ".git" in root or "node_modules" in root:
            continue
        for file in files:
            if file.endswith(".html") and file not in ["admin.html", "404.html"]:
                rel = os.path.relpath(os.path.join(root, file), ".").replace("\\", "/")
                urls.append(f"{DOMAIN}/" if rel == "index.html" else f"{DOMAIN}/{rel}")

print(f"Loaded {len(urls)} total URLs (including all 100 bot pages) for instant indexing.")

# 1. Submit full URL batch to IndexNow API (Bing, Yahoo, Yandex, Naver, Seznam)
payload = {
    "host": HOST,
    "key": INDEXNOW_KEY,
    "keyLocation": KEY_LOCATION,
    "urlList": urls
}

endpoints = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://yandex.com/indexnow"
]

headers = {"Content-Type": "application/json; charset=utf-8"}
data_bytes = json.dumps(payload).encode("utf-8")

for ep in endpoints:
    try:
        req = urllib.request.Request(ep, data=data_bytes, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"[SUCCESS] {ep} accepted all {len(urls)} URLs! (HTTP {resp.status})")
    except urllib.error.HTTPError as e:
        print(f"[INFO] {ep} returned HTTP {e.code}: {e.reason}")
    except Exception as e:
        print(f"[WARN] Could not reach {ep}: {e}")

# 2. Ping WebSub / PubSubHubbub & Sitemap Ping Endpoints for Google/Feed Crawlers
sitemap_url = urllib.parse.quote(f"{DOMAIN}/sitemap.xml")
ping_targets = [
    f"https://www.bing.com/ping?sitemap={sitemap_url}",
    "https://pubsubhubbub.appspot.com/"
]

for target in ping_targets:
    try:
        if "pubsubhubbub" in target:
            hub_data = urllib.parse.urlencode({
                "hub.mode": "publish",
                "hub.url": f"{DOMAIN}/sitemap.xml"
            }).encode("utf-8")
            req = urllib.request.Request(target, data=hub_data, method="POST")
        else:
            req = urllib.request.Request(target, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[PING OK] Notified {target} (HTTP {resp.status})")
    except Exception as e:
        print(f"[PING INFO] {target} response: {e}")

print("\nAll 100+ trading bot pages have been broadcast to search engine indexers!")
