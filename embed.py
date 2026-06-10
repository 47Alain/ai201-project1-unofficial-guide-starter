"""
embed.py — Milestone 4: Embedding + Vector Store
"""

import os
import sys
import json
import argparse

print("Starting embed.py...", flush=True)

try:
    from sentence_transformers import SentenceTransformer
    print("✓ sentence-transformers imported", flush=True)
except ImportError as e:
    print(f"✗ Missing sentence-transformers: {e}", flush=True)
    print("Run: pip install sentence-transformers", flush=True)
    sys.exit(1)

try:
    import chromadb
    print("✓ chromadb imported", flush=True)
except ImportError as e:
    print(f"✗ Missing chromadb: {e}", flush=True)
    print("Run: pip install chromadb", flush=True)
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "mit_unofficial_guide"
TOP_K           = 5
CHUNKS_FILE     = os.path.join("data", "chunks.json")
CHROMA_DIR      = os.path.join("data", "chroma")

os.makedirs(CHROMA_DIR, exist_ok=True)


def get_collection(client):
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def build_vector_store(force_rebuild=False):
    print("\n" + "=" * 60, flush=True)
    print("Building vector store...", flush=True)
    print("=" * 60, flush=True)

    # Load chunks
    if not os.path.exists(CHUNKS_FILE):
        print(f"✗ Chunks file not found: {CHUNKS_FILE}", flush=True)
        print("  Run: python chunk.py", flush=True)
        sys.exit(1)

    with open(CHUNKS_FILE, encoding="utf-8") as f:
        chunks = json.load(f)
    print(f"✓ Loaded {len(chunks)} chunks from {CHUNKS_FILE}", flush=True)

    # Connect to ChromaDB
    print(f"Connecting to ChromaDB at {CHROMA_DIR}...", flush=True)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = get_collection(client)
    existing = collection.count()
    print(f"✓ Collection '{COLLECTION_NAME}' has {existing} existing embeddings", flush=True)

    if existing == len(chunks) and not force_rebuild:
        print(f"\nVector store already up to date ({existing} embeddings).", flush=True)
        print("Use --rebuild to force a fresh build.", flush=True)
        return

    if force_rebuild and existing > 0:
        print(f"Rebuilding: deleting {existing} existing embeddings...", flush=True)
        client.delete_collection(COLLECTION_NAME)
        collection = get_collection(client)

    # Load model
    print(f"\nLoading embedding model: {EMBEDDING_MODEL}", flush=True)
    print("(First run downloads ~80MB — may take a minute)", flush=True)
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("✓ Model loaded", flush=True)

    # Embed in batches
    BATCH_SIZE = 64
    print(f"\nEmbedding {len(chunks)} chunks...", flush=True)

    for batch_start in range(0, len(chunks), BATCH_SIZE):
        batch      = chunks[batch_start : batch_start + BATCH_SIZE]
        texts      = [c["text"] for c in batch]
        ids        = [c["chunk_id"] for c in batch]
        metadatas  = [
            {
                "source_slug": c["source_slug"],
                "source_name": c["source_name"],
                "source_url":  c["source_url"],
                "chunk_index": str(c["chunk_index"]),
            }
            for c in batch
        ]
        embeddings = model.encode(texts, show_progress_bar=False).tolist()
        collection.add(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)

        end = min(batch_start + BATCH_SIZE, len(chunks))
        print(f"  Embedded {batch_start + 1}–{end} / {len(chunks)}", flush=True)

    print(f"\n✓ Done! {collection.count()} embeddings stored in {CHROMA_DIR}", flush=True)


def retrieve(query, k=TOP_K):
    client     = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = get_collection(client)

    if collection.count() == 0:
        print("✗ Vector store is empty. Run: python embed.py", flush=True)
        sys.exit(1)

    model     = SentenceTransformer(EMBEDDING_MODEL)
    query_emb = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_emb,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append({
            "text":        results["documents"][0][i],
            "source_name": results["metadatas"][0][i]["source_name"],
            "source_url":  results["metadatas"][0][i]["source_url"],
            "chunk_id":    results["ids"][0][i],
            "distance":    round(results["distances"][0][i], 4),
        })
    return chunks


def test_retrieval():
    test_queries = [
        "What grocery stores near MIT does the student guide recommend for produce and bulk grains?",
        "Does MIT offer free grocery shuttles, and which stores do they go to?",
        "What are the tradeoffs of living in a dining hall dorm vs cook-for-yourself dorm?",
        "What food assistance resources are available to MIT students who cannot afford food?",
        "What MBTA discount is available to MIT students and how much does it save?",
    ]

    print("\n" + "=" * 60, flush=True)
    print("RETRIEVAL TEST — 5 evaluation plan queries", flush=True)
    print("=" * 60, flush=True)

    for i, query in enumerate(test_queries, 1):
        print(f"\n── Query {i}: {query}", flush=True)
        results = retrieve(query, k=TOP_K)
        for rank, r in enumerate(results, 1):
            status = "✓" if r["distance"] < 0.5 else "⚠️ "
            print(f"  [{rank}] {status} distance={r['distance']:.4f}  |  {r['source_name']}", flush=True)
            print(f"       {r['text'][:180].replace(chr(10), ' ')}", flush=True)
        print(flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--query",   type=str)
    parser.add_argument("--test",    action="store_true")
    args = parser.parse_args()

    if args.query:
        print(f"\nQuery: {args.query}", flush=True)
        results = retrieve(args.query)
        for rank, r in enumerate(results, 1):
            status = "✓" if r["distance"] < 0.5 else "⚠️ "
            print(f"\n[{rank}] {status} distance={r['distance']:.4f}", flush=True)
            print(f"    source: {r['source_name']}", flush=True)
            print(f"    text:   {r['text'][:400]}", flush=True)
        return

    build_vector_store(force_rebuild=args.rebuild)

    if args.test:
        test_retrieval()
    else:
        print("\nNext steps:", flush=True)
        print("  Test all queries:  python embed.py --test", flush=True)
        print("  Single query:      python embed.py --query \"your question\"", flush=True)
        print("  Rebuild store:     python embed.py --rebuild", flush=True)


if __name__ == "__main__":
    main()
