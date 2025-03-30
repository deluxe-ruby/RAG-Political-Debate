from dotenv import load_dotenv
import os
from pinecone import Pinecone

load_dotenv()
pc = Pinecone(api_key=os.getenv(pcsk_37GnYh_JJmvdN29FMog87KLq8BQS4MGWeKed6i6z6ZyowTgogermJqQw2UPtBjzoraosph))
print("📦 Available indexes:", pc.list_indexes().names())
