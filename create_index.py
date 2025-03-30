from dotenv import load_dotenv
import os
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Create index
index_name = "political-debate"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",  # ✅ must be aws for free-tier
            region=os.getenv("PINECONE_ENV")  # should be us-west-2
        )
    )
    print(f"✅ Created index: {index_name}")
else:
    print(f"ℹ️ Index '{index_name}' already exists.")
