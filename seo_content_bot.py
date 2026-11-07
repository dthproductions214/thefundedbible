import os
import random
import datetime
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

KEYWORDS = [
    "Tradeify vs Apex Trader Funding 2026",
    "Best NinjaTrader 8 Indicators for Prop Firms",
    "How to Pass Prop Firm Evaluations Fast",
    "Top 5 Futures Prop Firms with No Scaling Plan",
    "Automated Trading Bots for Funded Accounts"
]

def generate_article():
    if not API_KEY:
        print("GEMINI_API_KEY not set. Skipping live AI generation.")
        return
    keyword = random.choice(KEYWORDS)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = keyword.lower().replace(" ", "-")
    
    prompt = f"""
    Write a highly engaging, SEO-optimized blog post in HTML format about '{keyword}'. 
    Target audience: Futures and forex traders looking for funded accounts and trading bots.
    Include a catchy H1 title, H2 subheadings, and a call-to-action at the end to buy 
    indicators and bots at thefundedbible.com. Do not include markdown code fences, just raw HTML.
    """
    
    print(f"Generating content for: {keyword}")
    response = model.generate_content(prompt)
    os.makedirs("articles", exist_ok=True)
    filepath = f"articles/{date_str}-{slug}.html"
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"Successfully created {filepath}")

if __name__ == "__main__":
    generate_article()
