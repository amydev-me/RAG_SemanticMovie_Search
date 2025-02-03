from pymongo import MongoClient
from embedding import generate_embedding
import os

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client[os.getenv("MONGO_DB_NAME")]
collection = db[os.getenv("MONGO_DB_COLLECTION_NAME")]

def create_plot_embeddings():
    """
    Generate embeddings for the 'plot' field in MongoDB and store them in the collection.
    """
    items = collection.find({'plot': {"$exists": True}}).limit(50)
    
    for doc in items:
        doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
        collection.replace_one({'_id': doc['_id']}, doc)
