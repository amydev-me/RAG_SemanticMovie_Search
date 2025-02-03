from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from embedding import generate_embedding
from plot_creation import create_plot_embeddings
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

uri = os.getenv("MONGO_URI")

client = MongoClient(uri)
db = client[os.getenv("MONGO_DB_NAME")]
collection = db[os.getenv("MONGO_DB_COLLECTION_NAME")]

@app.route('/search', methods=['POST'])
def search():
    """Perform vector search on MongoDB"""
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query text is required"}), 400

    query_embedding = generate_embedding(query)
    if query_embedding is None:
        return jsonify({"error": "Failed to generate embeddings"}), 500

    results = collection.aggregate([
        {
            '$vectorSearch': {
                'index': 'PlotSemanticSearch',
                'path': 'plot_embedding_hf',
                'queryVector': query_embedding,
                'numCandidates': 100,
                'limit': 8
            }
        }
    ])

    return jsonify({"data": [{"title": doc["title"], "plot": doc["plot"], "poster": doc.get("poster", None)} for doc in results]})

if __name__ == '__main__':
    create_plot_embeddings()  # Generate plot embeddings when the app starts
    app.run(debug=True)