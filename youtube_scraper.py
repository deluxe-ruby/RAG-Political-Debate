import os
import json
import openai
import uuid
from dotenv import load_dotenv
from pinecone import Pinecone
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import requests
import re

load_dotenv()

# Set up OpenAI and Pinecone
openai.api_key = os.getenv("OPENAI_API_KEY")
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("political-debate")

def get_video_ids_from_channel(channel_url):
    # Converts channel video page to uploads list (scrapes HTML for video IDs)
    response = requests.get(channel_url)
    if response.status_code != 200:
        print(f"❌ Failed to load: {channel_url}")
        return []

    html = response.text
    video_ids = re.findall(r"watch\?v=(\S{11})", html)
    return list(set(video_ids))[:5]  # Limit to 5 videos per run for now

def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([item['text'] for item in transcript])
        return text
    except Exception as e:
        print(f"⚠️ No transcript for {video_id}: {e}")
        return None

def embed_and_store(text, title, url):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embedding = response["data"][0]["embedding"]
    vector_id = str(uuid.uuid4())

    index.upsert(
        vectors=[(
            vector_id,
            embedding,
            {"title": title, "text": text, "source": url}
        )],
        namespace="left"
    )
    print(f"✅ Stored: {title}")

def load_youtube_sources():
    with open("sources.json", "r") as f:
        config = json.load(f)
    return config.get("left_sources", {}).get("youtube", [])

def run():
    for source in load_youtube_sources():
        print(f"🔍 Checking channel: {source['name']}")
        video_ids = get_video_ids_from_channel(source["url"])
        for vid in video_ids:
            url = f"https://www.youtube.com/watch?v={vid}"
            transcript = fetch_transcript(vid)
            if transcript:
                embed_and_store(transcript, f"YouTube Video: {vid}", url)

if __name__ == "__main__":
    run()
