import os
import re

# Swap this string anytime with your exact live $9 Stripe or Whop checkout URL
DIRECT_CHECKOUT_URL = "https://thefundedbible.com/vault.html?tier=bot9&price=9&promo=BIBLE80"

# Update all 100 bot pages + bots-catalog.html
updated_files = 0
for root, dirs, files in os.walk("."):
    if ".git" in root or "node_modules" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            orig = content
            # Ensure all $39 references are locked to $9
            content = content.replace("$39/mo", "$9/mo").replace("$39.00", "$9.00")
            content = re.sub(r'>\$39<', '>$9<', content)

            # Inject the 100 Bots Catalog link into index.html navigation bar if missing
            if file == "index.html" and "/bots-catalog.html" not in content:
                if "</nav>" in content:
                    content = content.replace(
                        "</nav>",
                        '    <a href="/bots-catalog.html" style="color:#10b981;font-weight:800;margin-left:18px;text-decoration:none;">100 Bots ($9)</a>\n</nav>',
                        1
                    )
                elif "vault.html" in content:
                    content = content.replace(
                        'href="vault.html"',
                        'href="/bots-catalog.html" style="color:#10b981;font-weight:800;margin-right:16px;">100 Bots ($9)</a> <a href="vault.html"',
                        1
                    )

            if content != orig:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                updated_files += 1

print(f"Patched {updated_files} HTML files with $9 checkout links and navbar link.")
