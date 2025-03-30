from dotenv import load_dotenv
import os

load_dotenv()
print("PINECONE_API_KEY =", os.getenv("PINECONE_API_KEY"))
