import os
import openai
import uuid
import argparse
from dotenv import load_dotenv
from pinecone import Pinecone

# Load API keys
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("political-debate")

def embed_and_store(text, title="Manual Submission", source="manual"):
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
            {"title": title, "text": text, "source": source}
        )],
        namespace="left"
    )
    print(f"✅ Stored with ID: {vector_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit a manual text file for embedding.")
    parser.add_argument("--file", help="Path to a .txt or .md file")
    args = parser.parse_args()

    if args.file and os.path.exists(args.file):
        with open(args.file, "r") as f:
            content = f.read()
        embed_and_store(content)
    else:
        print("❌ Please provide a valid text file with --file")
