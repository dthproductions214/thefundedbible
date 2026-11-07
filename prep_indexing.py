import os
import re

DOMAIN = "https://thefundedbible.com"
INDEXNOW_KEY = "tfb2026indexnowkey8899dthpropbots"

# Write the mandatory IndexNow verification key file in root
key_filename = f"{INDEXNOW_KEY}.txt"
with open(key_filename, "w", encoding="utf-8") as f:
    f.write(INDEXNOW_KEY)
print(f"Created IndexNow verification key file: {key_filename}")

# Ensure robots.txt exists and points directly to sitemap.xml
robots_content = f"""User-agent: *
Allow: /
Disallow: /admin.html

Sitemap: {DOMAIN}/sitemap.xml
"""
with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content)
print("Updated robots.txt with Sitemap directive.")
