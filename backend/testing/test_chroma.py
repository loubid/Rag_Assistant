import chromadb

client = chromadb.PersistentClient(
    path="data/vector_store/chroma_data"
)

collection = client.get_collection(
    name="harry_potter_pages"
)

print("Collection:", collection.name)
print("Number of chunks:", collection.count())

result = collection.get(
    limit=3,
    include=["documents", "metadatas"]
)

for i in range(len(result["ids"])):
    print("\n" + "=" * 60)
    print(f"CHUNK {i + 1}")
    print("=" * 60)

    print("ID:")
    print(result["ids"][i])

    print("\nMetadata:")
    print(result["metadatas"][i])

    print("\nDocument:")
    print(result["documents"][i][:500])