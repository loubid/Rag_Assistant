
from app.services.retrieval import Retriever


# Create Retriever
retriever = Retriever()


# Test question
question = "Who is Harry Potter?"


# Search ChromaDB
results = retriever.search(
    question=question,
    top_k=5
)


# Get results
documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


print("\n" + "=" * 70)
print("RETRIEVAL RESULTS")
print("=" * 70)


for i in range(len(documents)):

    print("\n" + "-" * 70)
    print(f"RESULT {i + 1}")
    print("-" * 70)

    print("Distance:", distances[i])

    print("\nMetadata:")
    print(metadatas[i])

    print("\nDocument:")
    print(documents[i][:1000])

