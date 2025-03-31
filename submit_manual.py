import argparse
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from uuid import uuid4

load_dotenv()

# Load API keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = "political-debate"

# Initialize clients
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

client = OpenAI(api_key=OPENAI_API_KEY)

# === Embed Text ===
def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

# === Parse File or URL ===
def parse_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    return "Manual Document", content

def parse_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.title.string.strip() if soup.title else "Untitled"
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    text = "\n".join(paragraphs)
    return title, text

# === Main ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to local text file")
    parser.add_argument("--url", help="URL to scrape")
    args = parser.parse_args()

    if args.file:
        title, text = parse_file(args.file)
    elif args.url:
        title, text = parse_url(args.url)
    else:
        print("❌ Must provide either --file or --url")
        exit(1)

    if not text.strip():
        print("⚠️ No text extracted. Skipping embedding.")
        exit(1)

    embedding = embed_text(text)
    vector_id = str(uuid4())

    index.upsert(vectors=[{
        "id": vector_id,
        "values": embedding,
        "metadata": {"title": title, "source": args.url or args.file}
    }])

    print(f"✅ Embedded article: \"{title}\"\n📌 Pinecone ID: {vector_id}")
