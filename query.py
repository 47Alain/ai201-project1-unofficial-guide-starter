"""
query.py — Milestone 5: Grounded Generation
Retrieves relevant chunks from ChromaDB, then asks Groq's LLM to answer
using ONLY those chunks as context. Source attribution is programmatically
guaranteed — sources are appended from metadata, not left to the LLM.

Usage (standalone test):
    python query.py "Does MIT offer free grocery shuttles?"

Imported by app.py:
    from query import ask
    result = ask("your question")
    # result = {"answer": "...", "sources": ["Source Name — URL", ...]}
"""

import os
import sys

# ── Load environment variables from .env ──────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # If python-dotenv not installed, rely on shell environment

# ── Dependencies ──────────────────────────────────────────────────────────────
try:
    from groq import Groq
except ImportError:
    raise SystemExit("Missing dependency. Run:  pip install groq")

try:
    from embed import retrieve
except ImportError:
    raise SystemExit("embed.py not found. Make sure it's in the same directory.")

# ── Config ────────────────────────────────────────────────────────────────────
MODEL   = "llama-3.3-70b-versatile"
TOP_K   = 5
MAX_TOKENS = 1024

# ── Grounding prompt ──────────────────────────────────────────────────────────
# This is the core of the RAG system. The system prompt strictly enforces
# that the LLM answers ONLY from the provided context chunks.
SYSTEM_PROMPT = """You are a helpful assistant for MIT students. You answer questions using ONLY the information provided in the context documents below.

Rules you must follow:
1. Answer ONLY from the provided context. Do not use outside knowledge.
2. If the context does not contain enough information to answer the question, respond with exactly: "I don't have enough information in my documents to answer that question."
3. Be specific and cite facts directly from the context.
4. Do not speculate, infer, or add information not present in the context.
5. Keep answers concise and practical — students want actionable information."""


def build_context(chunks: list[dict]) -> str:
    """Format retrieved chunks into a numbered context block for the prompt."""
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(
            f"[Document {i}: {chunk['source_name']}]\n{chunk['text']}"
        )
    return "\n\n---\n\n".join(parts)


def ask(question: str, k: int = TOP_K) -> dict:
    """
    Full RAG pipeline: retrieve → generate → return answer + sources.

    Returns:
        {
            "answer":  str,         # LLM response grounded in retrieved chunks
            "sources": list[str],   # "Source Name — URL" for each retrieved chunk
            "chunks":  list[dict],  # raw retrieved chunks (for debugging)
        }
    """
    # ── Step 1: Retrieve relevant chunks ──────────────────────────────────────
    chunks = retrieve(question, k=k)

    # ── Step 2: Build source list (programmatic — not left to LLM) ────────────
    # Deduplicate by source name while preserving order
    seen = set()
    sources = []
    for chunk in chunks:
        key = chunk["source_name"]
        if key not in seen:
            seen.add(key)
            sources.append(f"{chunk['source_name']} — {chunk['source_url']}")

    # ── Step 3: Build prompt with context ─────────────────────────────────────
    context = build_context(chunks)
    user_message = f"""Context documents:

{context}

---

Question: {question}

Answer using only the context documents above. If the answer isn't in the documents, say so."""

    # ── Step 4: Call Groq LLM ─────────────────────────────────────────────────
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {
            "answer": "Error: GROQ_API_KEY not found. Check your .env file.",
            "sources": sources,
            "chunks": chunks,
        }

    client = Groq(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
        )
        answer = response.choices[0].message.content.strip()

    except Exception as e:
        answer = f"Error calling Groq API: {e}"

    return {
        "answer":  answer,
        "sources": sources,
        "chunks":  chunks,
    }


# ── CLI test ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query.py \"your question here\"")
        print("\nRunning default test questions...\n")
        test_questions = [
            "Does MIT offer free grocery shuttles and which stores do they go to?",
            "What are the tradeoffs of living in a dining hall dorm vs cook-for-yourself?",
            "What is the best pizza place in Times Square?",  # out-of-scope test
        ]
    else:
        test_questions = [" ".join(sys.argv[1:])]

    for question in test_questions:
        print("=" * 60)
        print(f"Q: {question}")
        print("=" * 60)

        result = ask(question)

        print(f"\nANSWER:\n{result['answer']}")
        print(f"\nSOURCES ({len(result['sources'])}):")
        for s in result["sources"]:
            print(f"  • {s}")

        print(f"\nRETRIEVED CHUNKS (distances):")
        for chunk in result["chunks"]:
            print(f"  [{chunk['distance']:.4f}] {chunk['source_name']} — {chunk['chunk_id']}")
        print()
