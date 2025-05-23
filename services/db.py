from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "policy_db"
COLLECTION_NAME = "documents"

# Set up the client and collection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Save metadata when a document is uploaded
def save_document_metadata(filename, chunk_count):
    doc = {
        "filename": filename,
        "chunk_count": chunk_count,
        "created_at": datetime.datetime.utcnow()
    }
    result = collection.insert_one(doc)
    return str(result.inserted_id)

# Retrieve document by MongoDB ObjectId
def get_document_by_id(doc_id):
    return collection.find_one({"_id": ObjectId(doc_id)})
