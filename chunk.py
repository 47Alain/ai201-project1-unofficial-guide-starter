"""
chunk.py — Milestone 3: Chunking
Loads cleaned .txt files from data/raw/, splits them into 600-character chunks
with 100-character overlap, attaches source metadata, and saves to data/chunks.json.

Usage:
    python chunk.py

Output:
    data/chunks.json — list of chunk objects, each with:
        {
            "chunk_id":    "mitadmissions_dining_halls_004",
            "source_slug": "mitadmissions_dining_halls",
            "source_name": "MIT Admissions: Dining Halls (student blog)",
            "source_url":  "https://...",
            "chunk_index": 4,
            "text":        "..."
        }
"""

import os
import json

# ── Config — must match planning.md ──────────────────────────────────────────
CHUNK_SIZE    = 600   # characters per chunk
CHUNK_OVERLAP = 100   # characters of overlap between consecutive chunks
MIN_CHUNK_LEN = 50    # discard chunks shorter than this (fragments / empty)

RAW_DIR     = os.path.join("data", "raw")
OUTPUT_FILE = os.path.join("data", "chunks.json")

os.makedirs("data", exist_ok=True)


# ── Core chunking function ────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping character-level chunks.

    Strategy:
    - Slide a window of `chunk_size` characters across the text.
    - Each new chunk starts `chunk_size - overlap` characters after the previous one.
    - Snap chunk boundaries to the nearest sentence end ('. ', '! ', '? ', '\n')
      within a 60-character lookahead, so chunks don't cut mid-sentence.
    - Discard chunks shorter than MIN_CHUNK_LEN.

    Example with chunk_size=600, overlap=100:
        Chunk 0: chars   0–600
        Chunk 1: chars 500–1100   (starts 500 chars after chunk 0)
        Chunk 2: chars 1000–1600
        ...
    """
    chunks = []
    start = 0
    step = chunk_size - overlap   # 500 chars between chunk starts

    while start < len(text):
        end = start + chunk_size

        # Snap end to a nearby sentence boundary (within 60 chars lookahead)
        if end < len(text):
            snap_window = text[end : end + 60]
            for delim in (". ", "! ", "? ", "\n"):
                idx = snap_window.find(delim)
                if idx != -1:
                    end = end + idx + len(delim)
                    break

        chunk = text[start:end].strip()

        if len(chunk) >= MIN_CHUNK_LEN:
            chunks.append(chunk)

        start += step

    return chunks


# ── Load manifest ─────────────────────────────────────────────────────────────

def load_manifest() -> list[dict]:
    manifest_path = os.path.join(RAW_DIR, "manifest.json")
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(
            f"Manifest not found at {manifest_path}. "
            "Run  python ingest.py  first."
        )
    with open(manifest_path, encoding="utf-8") as f:
        return json.load(f)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("MIT Unofficial Guide — Chunking (chunk.py)")
    print(f"Chunk size: {CHUNK_SIZE} chars | Overlap: {CHUNK_OVERLAP} chars")
    print("=" * 60)

    manifest = load_manifest()
    all_chunks = []
    source_stats = []

    for entry in manifest:
        if entry["status"] != "ok":
            print(f"\n[{entry['id']:02d}] SKIP (failed ingestion): {entry['name']}")
            continue

        file_path = entry["file"]
        if not os.path.exists(file_path):
            print(f"\n[{entry['id']:02d}] SKIP (file missing): {file_path}")
            continue

        with open(file_path, encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        n = len(chunks)
        print(f"\n[{entry['id']:02d}] {entry['name']}")
        print(f"     {len(text):,} chars → {n} chunks")

        for i, chunk_text_val in enumerate(chunks):
            all_chunks.append({
                "chunk_id":    f"{entry['slug']}_{i:03d}",
                "source_slug": entry["slug"],
                "source_name": entry["name"],
                "source_url":  entry["url"],
                "chunk_index": i,
                "text":        chunk_text_val,
            })

        source_stats.append({"name": entry["name"], "chunks": n})

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    total = len(all_chunks)
    print("\n" + "=" * 60)
    print(f"DONE: {total} total chunks from {len(source_stats)} sources.")
    print(f"Saved → {OUTPUT_FILE}")

    # Health check
    print("\n── Health check ──────────────────────────────────────────")
    if total < 50:
        print("⚠️  WARNING: Fewer than 50 chunks total. Chunks may be too large,")
        print("   or some documents failed to load. Check manifest.json.")
    elif total > 2000:
        print("⚠️  WARNING: More than 2,000 chunks total. Chunks may be too small.")
    else:
        print(f"✓  Chunk count ({total}) is in the healthy range (50–2000).")

    # Print 5 sample chunks for manual inspection
    print("\n── 5 sample chunks (inspect for quality) ─────────────────")
    import random
    samples = random.sample(all_chunks, min(5, total))
    for s in samples:
        print(f"\n  [chunk_id: {s['chunk_id']}]")
        print(f"  source: {s['source_name']}")
        print(f"  length: {len(s['text'])} chars")
        print(f"  text preview:\n    {s['text'][:300].replace(chr(10), ' ')!r}")
    
    print("\nNext step: run  python embed.py")


if __name__ == "__main__":
    main()