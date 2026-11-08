import os
import re
from datetime import datetime

ROOT_DIR = "."
DOMAIN = "https://thefundedbible.com"

def fix_html_files():
    fixed_count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        if ".git" in root or "node_modules" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                original_content = content

                # Strip out the top CME live ticker bar
                content = re.sub(
                    r'<!--\s*CME TICKER START\s*-->.*?<!--\s*CME TICKER END\s*-->',
                    '',
                    content,
                    flags=re.DOTALL | re.IGNORECASE
                )
                content = re.sub(
                    r'<div[^>]*id=["\'](?:cme-ticker|top-ticker|live-ticker)["\'][^>]*>.*?</div>',
                    '',
                    content,
                    flags=re.DOTALL | re.IGNORECASE
                )

                # Fix pricing display discrepancies ($39 -> $9)
                content = content.replace("$39/mo", "$9/mo")
                content = content.replace("$39.00", "$9.00")
                content = re.sub(r'>\$39<', '>$9<', content)

                if content != original_content:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    fixed_count += 1
                    print(f"Fixed: {filepath}")

    print(f"Total HTML files patched: {fixed_count}")

def rebuild_sitemap():
    urls = []
    today = datetime.now().strftime("%Y-%m-%d")
    for root, dirs, files in os.walk(ROOT_DIR):
        if ".git" in root or "node_modules" in root:
            continue
        for file in files:
            if file.endswith(".html") and file not in ["admin.html", "404.html"]:
                rel_path = os.path.relpath(os.path.join(root, file), ROOT_DIR).replace("\\", "/")
                url = f"{DOMAIN}/" if rel_path == "index.html" else f"{DOMAIN}/{rel_path}"
                priority = "1.0" if rel_path == "index.html" else "0.8"
                urls.append((url, today, priority))

    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, lastmod, priority in sorted(urls):
        sitemap_xml += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <priority>{priority}</priority>\n  </url>\n"
    sitemap_xml += "</urlset>"

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print(f"Sitemap rebuilt with {len(urls)} active pages.")

if __name__ == "__main__":
    fix_html_files()
    rebuild_sitemap()
