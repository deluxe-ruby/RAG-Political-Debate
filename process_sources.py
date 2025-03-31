import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import openai

# Load API keys
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load source config
with open("sources.json") as f:
    sources = json.load(f)

# Process each source
for source in sources:
    print(f"🔍 Processing source: {source['source_name']}")

    if source["type"] == "web":
        print(f"🌐 Scraping {source['url']} using {source['parser']} parser...")
        response = requests.get(source["url"])
        soup = BeautifulSoup(response.content, "html.parser")
        article_text = " ".join([p.get_text() for p in soup.find_all("p")])

        print(f"📄 Article text (first 500 chars): {article_text[:500]}")

        # Summarize with OpenAI
        if client.api_key:
            print("🔎 Asking OpenAI for summary...")
            chat_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Summarize this article for a progressive audience."},
                    {"role": "user", "content": article_text}
                ]
            )
            print(f"📝 Summary:\n{chat_response.choices[0].message.content}")

    elif source["type"] == "youtube":
        print(f"📺 Processing YouTube channel ID: {source['channel_id']} using {source['transcript_method']}...")

        # Build the Uploads playlist URL
        channel_id = source['channel_id']
        if channel_id.startswith("UC"):
            playlist_url = f"https://www.youtube.com/playlist?list=UU{channel_id[2:]}"
        else:
            playlist_url = f"https://www.youtube.com/@{channel_id}"

        ydl_opts = {
            'quiet': True,
            'extract_flat': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(playlist_url, download=False)
                for video in result.get('entries', [])[:2]:  # Just show 2 for now
                    video_id = video.get("id")
                    video_title = video.get("title", "Untitled")
                    video_url = f"https://www.youtube.com/watch?v={video_id}"

                    print(f"📹 Found video: {video_title}")
                    print(f"🔗 URL: {video_url}")

                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video_id)
                        transcript_text = " ".join([entry["text"] for entry in transcript])
                        print(f"📜 Transcript (first 300 chars): {transcript_text[:300]}...")

                        # Summarize with OpenAI
                        print("🔎 Asking OpenAI for transcript summary...")
                        chat_response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "Summarize this YouTube transcript for a progressive audience."},
                                {"role": "user", "content": transcript_text}
                            ]
                        )
                        print(f"📝 Summary:\n{chat_response.choices[0].message.content}")

                    except Exception as e:
                        print(f"❌ Could not get transcript for {video_id}: {e}")

        except Exception as e:
            print(f"❌ Failed to process YouTube channel: {e}")

    else:
        print(f"❓ Unknown source type: {source['type']}")
