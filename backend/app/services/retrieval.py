from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

CHROMA_PATH = BASE_DIR / "data" / "vector_store" / "chroma_data"

COLLECTION_NAME = "harry_potter_pages"

MODEL_NAME = "intfloat/multilingual-e5-large"


# --------------------------------------------------
# Retriever
# --------------------------------------------------

class Retriever:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
        MODEL_NAME,
        device="cuda"
        )
        print("Embedding model loaded.")

        print("Loading ChromaDB...")

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PATH)
        )

        self.collection = self.client.get_collection(
            name=COLLECTION_NAME
        )

        print("ChromaDB loaded successfully.")
        print(f"Collection: {self.collection.name}")
        print(f"Chunks: {self.collection.count()}")

    def search(self, question: str, top_k: int = 5):

        # E5 models require the "query:" prefix for questions
        query_text = f"query: {question}"

        # Generate query embedding
        query_embedding = self.model.encode(
            [query_text],
            normalize_embeddings=True
        )[0].tolist()

        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        return results

