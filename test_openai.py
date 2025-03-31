import openai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Test chat completion with v1-style client
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, OpenAI!"}]
    )
    print("✅ OpenAI API is working!")
    print("Response:", response.choices[0].message.content)

except Exception as e:
    print("❌ Something went wrong:", e)
