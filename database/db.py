from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
import datetime

def get_db():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        print("MONGO_URI not found in environment variables")
        return None
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        print("Connected to MongoDB Atlas")
        return client.get_default_database()
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"MongoDB connection failed: {e}")
        return None

def save_analysis(data):
    try:
        db = get_db()
        if db is None:
            print("Skipping database save - MongoDB not available")
            return
        collection = db['analyses']
        collection.insert_one(data)
    except Exception as e:
        print(f"Error saving to database: {e}")

def get_history():
    try:
        db = get_db()
        if db is None:
            print("Skipping database fetch - MongoDB not available")
            return []
        collection = db['analyses']
        # Return last 10 analyses, sorted by timestamp desc
        cursor = collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(10)
        return list(cursor)
    except Exception as e:
        print(f"Error fetching history: {e}")
        return []
