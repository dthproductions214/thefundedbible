import os
import re
import json
import urllib.request
import urllib.error

HOST = "www.thefundedbible.com"
SITE_URL = f"https://{HOST}"
KEY = "tfb2026indexnowkey87dth9942"
KEY_LOCATION = f"{SITE_URL}/{KEY}.txt"

def extract_urls_from_sitemap():
    if not os.path.exists("sitemap.xml"):
        return [f"{SITE_URL}/"]
    with open("sitemap.xml", "r", encoding="utf-8") as f:
        content = f.read()
    urls = re.findall(r"<loc>(.*?)</loc>", content)
    if f"{SITE_URL}/directory.html" not in urls:
        urls.append(f"{SITE_URL}/directory.html")
    return sorted(list(set(urls)))

def build_html_crawl_directory(urls):
    links_html = ""
    for u in urls:
        slug = u.replace(f"{SITE_URL}/", "") or "index.html (Live Command Desk)"
        clean_label = slug.replace(".html", "").replace("-", " ").upper()
        links_html += f'<a href="{u}" style="background:#070b14;border:1px solid rgba(245,158,11,0.25);padding:10px 14px;border-radius:8px;color:#f8fafc;text-decoration:none;font-family:\'JetBrains Mono\',monospace;font-size:11px;display:flex;justify-content:space-between;align-items:center;"><span>{clean_label}</span><span style="color:#10b981;">→</span></a>\n'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>COMPLETE SITE DIRECTORY &amp; PROP FIRM AUDIT INDEX | The Funded Bible™</title>
  <meta name="description" content="Complete index of all {len(urls)} verified futures prop firm comparisons, drawdown calculators, and daily NY Open execution briefings on The Funded Bible." />
  <link rel="canonical" href="{SITE_URL}/directory.html" />
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Space+Grotesk:wght@700;800&display=swap" rel="stylesheet">
</head>
<body style="background:#030508;color:#f8fafc;font-family:'Space Grotesk',sans-serif;margin:0;padding:36px 20px 80px;">
  <main style="max-width:1320px;margin:0 auto;">
    <div style="margin-bottom:24px;border-bottom:1px solid rgba(245,158,11,0.35);padding-bottom:18px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
      <div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#10b981;font-weight:800;">● COMPLETE SEARCH ENGINE CRAWL HUB ({len(urls)} LIVE PAGES)</div>
        <h1 style="font-size:30px;margin:6px 0 0;">The Funded Bible™ Master Audit Index</h1>
      </div>
      <a href="index.html" style="background:#f59e0b;color:#000;font-family:'JetBrains Mono',monospace;font-weight:800;font-size:12px;padding:10px 16px;border-radius:6px;text-decoration:none;">← BACK TO LIVE TERMINAL</a>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px;">
      {links_html}
    </div>
  </main>
</body>
</html>"""
    with open("directory.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[✓] Built directory.html with {len(urls)} direct internal crawl links for Googlebot.")

def submit_indexnow_batch(urls):
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls
    }
    data = json.dumps(payload).encode("utf-8")
    endpoints = [
        "https://api.indexnow.org/indexnow",
        "https://www.bing.com/indexnow",
        "https://yandex.com/indexnow"
    ]
    for ep in endpoints:
        try:
            req = urllib.request.Request(
                ep,
                data=data,
                headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "TheFundedBible-SEO-Bot/1.0"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                print(f"[✓] IndexNow Batch Submitted -> {ep} | Status: HTTP {resp.status} ({len(urls)} URLs)")
        except urllib.error.HTTPError as e:
            print(f"[i] IndexNow Response -> {ep} | HTTP {e.code} ({e.reason})")
        except Exception as ex:
            print(f"[!] Warning on {ep}: {ex}")

if __name__ == "__main__":
    all_urls = extract_urls_from_sitemap()
    build_html_crawl_directory(all_urls)
    submit_indexnow_batch(all_urls)