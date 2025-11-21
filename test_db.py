import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('backend/.env')

mongo_uri = os.getenv("MONGO_URI")
print(f"Testing connection to: {mongo_uri}")

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("SUCCESS: Connected to MongoDB Atlas")
    db = client.get_default_database()
    print(f"Database: {db.name}")
except Exception as e:
    print(f"FAILURE: {e}")
