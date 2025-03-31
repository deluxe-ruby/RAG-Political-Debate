import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai

# Load keys
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Target article (from Reich's Substack)
URL = "https://robertreich.substack.com/p/the-supreme-court-versus-the-constitution"

# Scrape article
response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
article_text = " ".join([p.get_text() for p in soup.find_all("p")])

print("✅ Scraped article text (first 500 chars):")
print(article_text[:500] + "...")

# Optional: Summarize with OpenAI
if os.getenv("OPENAI_API_KEY"):
    print("\n🔎 Asking OpenAI for summary...")
    chat_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize this article for a progressive audience."},
            {"role": "user", "content": article_text}
        ]
    )
    print("\n📝 Summary:")
    print(chat_response.choices[0].message.content)
else:
    print("❌ OPENAI_API_KEY not found!")
