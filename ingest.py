# """
# ingest.py — Milestone 3: Document Ingestion
# Fetches all 15 source URLs, strips HTML/boilerplate, saves cleaned text to data/raw/.

# Usage:
#     python ingest.py

# Output:
#     data/raw/<slug>.txt for each source
#     data/raw/manifest.json — records source name, URL, and output filename
# """

# import os
# import json
# import time
# import re
# import requests
# from bs4 import BeautifulSoup

# # ── Output directory ───────────────────────────────────────────────────────────
# RAW_DIR = os.path.join("data", "raw")
# os.makedirs(RAW_DIR, exist_ok=True)

# # ── Source documents (from planning.md) ────────────────────────────────────────
# SOURCES = [
#     {
#         "id": 1,
#         "slug": "mit_food_resource_guide",
#         "name": "MIT Food Resource Guide (UAC)",
#         "url": "https://advising.mit.edu/fli/resources/food-resource-guide/",
#     },
#     {
#         "id": 2,
#         "slug": "mit_oge_low_cost_resources",
#         "name": "MIT Free & Low-Cost Student Resources (OGE)",
#         "url": "https://oge.mit.edu/student-support-development/free-low-cost-student-resources",
#     },
#     {
#         "id": 3,
#         "slug": "mit_grocery_shuttle_schedule",
#         "name": "MIT Grocery Shuttle Schedule",
#         "url": "https://web.mit.edu/Facilities/transportation/shuttles/grocery.html",
#     },
#     {
#         "id": 4,
#         "slug": "mitadmissions_dining_halls",
#         "name": "MIT Admissions: Dining Halls (student blog)",
#         "url": "https://mitadmissions.org/blogs/entry/mit-dining-halls/",
#     },
#     {
#         "id": 5,
#         "slug": "mitadmissions_cook_for_yourself",
#         "name": "MIT Admissions: How to Survive in a Cook-for-Yourself Community",
#         "url": "https://mitadmissions.org/blogs/entry/how-to-survive-in-a-cook-for-yourself-community/",
#     },
#     {
#         "id": 6,
#         "slug": "mitadmissions_groceries_guide",
#         "name": "MIT Admissions: Groceries Guide (guest post)",
#         "url": "https://mitadmissions.org/blogs/entry/where-to-buy-food-mit-groceries-guide/",
#     },
#     {
#         "id": 7,
#         "slug": "mitadmissions_choosing_dorm",
#         "name": "MIT Admissions: Guide to Choosing a Dorm",
#         "url": "https://mitadmissions.org/blogs/entry/how-to-not-choose-a-dorm/",
#     },
#     {
#         "id": 8,
#         "slug": "mitadmissions_dorm_social_life",
#         "name": "MIT Admissions: How Dorm Structure Shapes Social Life",
#         "url": "https://mitadmissions.org/blogs/entry/how-dorm-structure-shapes-social-life/",
#     },
#     {
#         "id": 9,
#         "slug": "mitadmissions_starting_first_year",
#         "name": "MIT Admissions: Starting Your First Year",
#         "url": "https://mitadmissions.org/blogs/entry/so-youre-starting-your-first-year/",
#     },
#     {
#         "id": 10,
#         "slug": "mitadmissions_things_i_wish_i_knew",
#         "name": "MIT Admissions: Things I Wish I Knew",
#         "url": "https://mitadmissions.org/blogs/entry/some-things-i-wish-i-knew-coming-in/",
#     },
#     {
#         "id": 11,
#         "slug": "mitadmissions_survival_guide",
#         "name": "MIT Admissions: An MIT Survival Guide",
#         "url": "https://mitadmissions.org/blogs/entry/an_mit_survival_guide/",
#     },
#     {
#         "id": 12,
#         "slug": "mitadmissions_dining_overview",
#         "name": "MIT Admissions: Dining at MIT (overview)",
#         "url": "https://mitadmissions.org/blogs/entry/dining-at-mit/",
#     },
#     {
#         "id": 13,
#         "slug": "mit_iso_food_resources",
#         "name": "MIT ISO: Food Resources for International Students",
#         "url": "https://iso.mit.edu/?p=293",
#     },
#     {
#         "id": 14,
#         "slug": "mit_news_techmart",
#         "name": "MIT News: TechMart At-Cost Grocery Store",
#         "url": "https://news.mit.edu/2018/mit-techmart-at-cost-grocery-store-pilot-opens-in-walker-memorial-0926",
#     },
#     {
#         "id": 15,
#         "slug": "reddit_mit_dorms_freshman",
#         "name": "Reddit r/mit: Incoming Freshman Wondering About Dorms",
#         "url": "https://www.reddit.com/r/mit/comments/1iz9648/incoming_freshman_wondering_about_dorms_at_mit/",
#         "is_reddit": True,
#     },
# ]

# # ── Boilerplate patterns to strip (plain text, post-BeautifulSoup) ─────────────
# BOILERPLATE_PATTERNS = [
#     r"Skip to (main )?content",
#     r"Cookie (Policy|Settings|Banner)",
#     r"Accept (All )?Cookies",
#     r"Read more",
#     r"Keep Reading",
#     r"Share (on|via) \w+",
#     r"^\s*\d+ (comments?|shares?|likes?)\s*$",
#     r"Subscribe to",
#     r"Sign (up|in) (to|for)",
#     r"Follow us",
#     r"©\s*\d{4}",
#     r"All rights reserved",
#     r"Privacy Policy",
#     r"Terms of (Use|Service)",
#     r"^\s*\[\d+\]\s*$",          # bare footnote markers like [1]
#     r"⁠\d+",                     # MIT blog inline footnote markers
#     r"^\s*·\s*$",                # lone bullet separators
# ]

# BOILERPLATE_RE = re.compile(
#     "|".join(f"({p})" for p in BOILERPLATE_PATTERNS),
#     re.IGNORECASE | re.MULTILINE,
# )


# def fetch_html(url: str, is_reddit: bool = False) -> str:
#     """Fetch raw HTML from a URL. Uses Reddit's JSON API for Reddit threads."""
#     headers = {
#         "User-Agent": (
#             "Mozilla/5.0 (compatible; MIT-RAG-Project/1.0; "
#             "educational use only)"
#         )
#     }
#     if is_reddit:
#         # Reddit's JSON API: append .json to the thread URL
#         json_url = url.rstrip("/") + ".json?limit=100"
#         resp = requests.get(json_url, headers=headers, timeout=15)
#         resp.raise_for_status()
#         return resp.text  # raw JSON string, handled separately
#     else:
#         resp = requests.get(url, headers=headers, timeout=15)
#         resp.raise_for_status()
#         return resp.text


# def parse_reddit_json(raw_json: str) -> str:
#     """
#     Extract comment text from Reddit's JSON API response.
#     Keeps: post title, post selftext, top-level comments with score >= 2.
#     Discards: mod comments, deleted/removed content, deeply nested replies.
#     """
#     data = json.loads(raw_json)
#     parts = []

#     # Post title and body
#     post = data[0]["data"]["children"][0]["data"]
#     parts.append(f"POST TITLE: {post.get('title', '')}")
#     if post.get("selftext"):
#         parts.append(post["selftext"])

#     # Top-level comments
#     comments = data[1]["data"]["children"]
#     for child in comments:
#         c = child.get("data", {})
#         if child.get("kind") != "t1":
#             continue
#         score = c.get("score", 0)
#         body = c.get("body", "").strip()
#         # Skip low-score, deleted, or mod-only comments
#         if score < 2 or body in ("[deleted]", "[removed]", ""):
#             continue
#         parts.append(f"[Comment, score={score}] {body}")

#     return "\n\n".join(parts)


# def clean_html(html: str, url: str) -> str:
#     """
#     Parse HTML with BeautifulSoup and extract substantive text.
#     Removes: nav, header, footer, aside, script, style, cookie banners.
#     Keeps: article body, main content, paragraphs, lists.
#     """
#     soup = BeautifulSoup(html, "html.parser")

#     # Remove structural noise tags entirely
#     for tag in soup.find_all(
#         ["nav", "header", "footer", "aside", "script", "style",
#          "noscript", "form", "button", "iframe", "svg", "figure"]
#     ):
#         tag.decompose()

#     # Remove elements by common boilerplate class/id names
#     boilerplate_selectors = [
#         "[class*='cookie']", "[class*='banner']", "[class*='popup']",
#         "[class*='modal']", "[class*='sidebar']", "[class*='menu']",
#         "[class*='nav']", "[class*='footer']", "[class*='header']",
#         "[class*='share']", "[class*='social']", "[class*='ad']",
#         "[class*='comment-count']", "[id*='cookie']", "[id*='nav']",
#         "[id*='footer']", "[id*='header']", "[id*='sidebar']",
#     ]
#     for selector in boilerplate_selectors:
#         for el in soup.select(selector):
#             el.decompose()

#     # Extract text — prefer <main> or <article> if present, fall back to <body>
#     main = soup.find("main") or soup.find("article") or soup.find("body")
#     if main is None:
#         return ""

#     text = main.get_text(separator="\n")
#     return text


# def clean_text(raw: str) -> str:
#     """
#     Post-process extracted text:
#     - Decode HTML entities (BeautifulSoup handles most, this catches leftovers)
#     - Strip boilerplate lines
#     - Collapse excessive whitespace
#     """
#     # Remove boilerplate patterns line by line
#     lines = raw.splitlines()
#     cleaned = []
#     for line in lines:
#         line = line.strip()
#         if not line:
#             cleaned.append("")
#             continue
#         if BOILERPLATE_RE.search(line):
#             continue
#         # Drop lines that are just punctuation or very short noise
#         if len(line) < 3 and not line.isdigit():
#             continue
#         cleaned.append(line)

#     text = "\n".join(cleaned)

#     # Collapse 3+ blank lines into 2
#     text = re.sub(r"\n{3,}", "\n\n", text)

#     # Remove leftover HTML entities
#     text = text.replace("&amp;", "&").replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'").replace("&quot;", '"')

#     return text.strip()


# def ingest_source(source: dict) -> dict:
#     """Fetch, parse, clean, and save one source. Returns a manifest entry."""
#     slug = source["slug"]
#     url = source["url"]
#     is_reddit = source.get("is_reddit", False)
#     out_path = os.path.join(RAW_DIR, f"{slug}.txt")

#     print(f"\n[{source['id']:02d}] Fetching: {source['name']}")
#     print(f"     URL: {url}")

#     try:
#         raw = fetch_html(url, is_reddit=is_reddit)

#         if is_reddit:
#             text = parse_reddit_json(raw)
#         else:
#             text = clean_html(raw, url)

#         text = clean_text(text)

#         if len(text) < 100:
#             print(f"     ⚠️  WARNING: Very short output ({len(text)} chars) — check this source manually.")

#         with open(out_path, "w", encoding="utf-8") as f:
#             f.write(text)

#         char_count = len(text)
#         print(f"     ✓  Saved {char_count:,} characters → {out_path}")

#         return {
#             "id": source["id"],
#             "slug": slug,
#             "name": source["name"],
#             "url": url,
#             "file": out_path,
#             "char_count": char_count,
#             "status": "ok",
#         }

#     except Exception as e:
#         print(f"     ✗  FAILED: {e}")
#         return {
#             "id": source["id"],
#             "slug": slug,
#             "name": source["name"],
#             "url": url,
#             "file": None,
#             "char_count": 0,
#             "status": f"error: {e}",
#         }


# def main():
#     print("=" * 60)
#     print("MIT Unofficial Guide — Document Ingestion (ingest.py)")
#     print("=" * 60)

#     manifest = []
#     for source in SOURCES:
#         entry = ingest_source(source)
#         manifest.append(entry)
#         # Be polite to servers — don't hammer them
#         time.sleep(1.5)

#     # Save manifest
#     manifest_path = os.path.join(RAW_DIR, "manifest.json")
#     with open(manifest_path, "w", encoding="utf-8") as f:
#         json.dump(manifest, f, indent=2)

#     # Summary
#     ok = [e for e in manifest if e["status"] == "ok"]
#     failed = [e for e in manifest if e["status"] != "ok"]

#     print("\n" + "=" * 60)
#     print(f"DONE: {len(ok)}/{len(manifest)} sources ingested successfully.")
#     if failed:
#         print(f"\nFAILED SOURCES ({len(failed)}):")
#         for e in failed:
#             print(f"  [{e['id']}] {e['name']}: {e['status']}")
#     print(f"\nManifest saved to: {manifest_path}")
#     print("\nNext step: run  python chunk.py")


# if __name__ == "__main__":
#     main()


"""
ingest.py — Milestone 3: Document Ingestion
Fetches URLs where possible; for JS-blocked sites, loads manually saved .txt files.

Usage:
    python ingest.py

Output:
    data/raw/<slug>.txt for each source
    data/raw/manifest.json
"""

import os
import json
import time
import re
import requests
from bs4 import BeautifulSoup

RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

SOURCES = [
    {"id": 1,  "slug": "mit_food_resource_guide",              "name": "MIT Food Resource Guide (UAC)",                              "url": "https://advising.mit.edu/fli/resources/food-resource-guide/",           "manual": True},
    {"id": 2,  "slug": "mit_oge_low_cost_resources",           "name": "MIT Free & Low-Cost Student Resources (OGE)",               "url": "https://oge.mit.edu/student-support-development/free-low-cost-student-resources"},
    {"id": 3,  "slug": "mit_grocery_shuttle_schedule",         "name": "MIT Grocery Shuttle Schedule",                              "url": "https://web.mit.edu/Facilities/transportation/shuttles/grocery.html"},
    {"id": 4,  "slug": "mitadmissions_dining_halls",           "name": "MIT Admissions: Dining Halls (student blog)",               "url": "https://mitadmissions.org/blogs/entry/mit-dining-halls/",               "manual": True},
    {"id": 5,  "slug": "mitadmissions_cook_for_yourself",      "name": "MIT Admissions: Cook-for-Yourself Community",               "url": "https://mitadmissions.org/blogs/entry/how-to-survive-in-a-cook-for-yourself-community/", "manual": True},
    {"id": 6,  "slug": "mitadmissions_groceries_guide",        "name": "MIT Admissions: Groceries Guide",                           "url": "https://mitadmissions.org/blogs/entry/where-to-buy-food-mit-groceries-guide/", "manual": True},
    {"id": 7,  "slug": "mitadmissions_choosing_dorm",          "name": "MIT Admissions: Guide to Choosing a Dorm",                  "url": "https://mitadmissions.org/blogs/entry/how-to-not-choose-a-dorm/",       "manual": True},
    {"id": 8,  "slug": "mitadmissions_dorm_social_life",       "name": "MIT Admissions: How Dorm Structure Shapes Social Life",     "url": "https://mitadmissions.org/blogs/entry/how-dorm-structure-shapes-social-life/", "manual": True},
    {"id": 9,  "slug": "mitadmissions_starting_first_year",    "name": "MIT Admissions: Starting Your First Year",                  "url": "https://mitadmissions.org/blogs/entry/so-youre-starting-your-first-year/", "manual": True},
    {"id": 10, "slug": "mitadmissions_things_i_wish_i_knew",   "name": "MIT Admissions: Things I Wish I Knew",                     "url": "https://mitadmissions.org/blogs/entry/some-things-i-wish-i-knew-coming-in/", "manual": True},
    {"id": 11, "slug": "mitadmissions_survival_guide",         "name": "MIT Admissions: An MIT Survival Guide",                    "url": "https://mitadmissions.org/blogs/entry/an_mit_survival_guide/",          "manual": True},
    {"id": 12, "slug": "mitadmissions_dining_overview",        "name": "MIT Admissions: Dining at MIT (overview)",                  "url": "https://mitadmissions.org/blogs/entry/dining-at-mit/",                 "manual": True},
    {"id": 13, "slug": "mit_iso_food_resources",               "name": "MIT ISO: Food Resources for International Students",        "url": "https://iso.mit.edu/?p=293"},
    {"id": 14, "slug": "mit_news_techmart",                    "name": "MIT News: TechMart At-Cost Grocery Store",                  "url": "https://news.mit.edu/2018/mit-techmart-at-cost-grocery-store-pilot-opens-in-walker-memorial-0926"},
    {"id": 15, "slug": "reddit_mit_dorms_freshman",            "name": "Reddit r/mit: Incoming Freshman Wondering About Dorms",     "url": "https://www.reddit.com/r/mit/comments/1iz9648/incoming_freshman_wondering_about_dorms_at_mit/", "manual": True},
]

BOILERPLATE_PATTERNS = [
    r"Skip to (main )?content", r"Cookie (Policy|Settings|Banner)", r"Accept (All )?Cookies",
    r"Read more", r"Keep Reading", r"Share (on|via) \w+",
    r"^\s*\d+ (comments?|shares?|likes?)\s*$", r"Subscribe to", r"Sign (up|in) (to|for)",
    r"Follow us", r"©\s*\d{4}", r"All rights reserved", r"Privacy Policy",
    r"Terms of (Use|Service)", r"^\s*\[\d+\]\s*$", r"⁠\d+", r"^\s*·\s*$",
]
BOILERPLATE_RE = re.compile("|".join(f"({p})" for p in BOILERPLATE_PATTERNS), re.IGNORECASE | re.MULTILINE)


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["nav", "header", "footer", "aside", "script", "style", "noscript", "form", "button", "iframe", "svg"]):
        tag.decompose()
    for selector in ["[class*='cookie']","[class*='banner']","[class*='nav']","[class*='footer']","[class*='header']","[class*='sidebar']","[class*='share']","[class*='social']"]:
        for el in soup.select(selector):
            el.decompose()
    main = soup.find("main") or soup.find("article") or soup.find("body")
    return main.get_text(separator="\n") if main else ""


def clean_text(raw: str) -> str:
    lines = raw.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line:
            cleaned.append("")
            continue
        if BOILERPLATE_RE.search(line):
            continue
        if len(line) < 3:
            continue
        cleaned.append(line)
    text = "\n".join(cleaned)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.replace("&amp;","&").replace("&nbsp;"," ").replace("&#39;","'").replace("&quot;",'"')
    return text.strip()


def ingest_source(source: dict) -> dict:
    slug = source["slug"]
    out_path = os.path.join(RAW_DIR, f"{slug}.txt")
    is_manual = source.get("manual", False)

    print(f"\n[{source['id']:02d}] {source['name']}")

    # ── Manual sources: load existing file if present, otherwise warn ──────────
    if is_manual:
        if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
            with open(out_path, encoding="utf-8") as f:
                raw = f.read()
            text = clean_text(raw)
            # Re-save cleaned version
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"     ✓  Manual file found & cleaned → {len(text):,} chars")
            return {"id": source["id"], "slug": slug, "name": source["name"],
                    "url": source["url"], "file": out_path, "char_count": len(text), "status": "ok"}
        else:
            print(f"     ⏳ NEEDS MANUAL COPY — visit: {source['url']}")
            print(f"        Save text to: {out_path}")
            return {"id": source["id"], "slug": slug, "name": source["name"],
                    "url": source["url"], "file": None, "char_count": 0, "status": "needs_manual_copy"}

    # ── Auto-fetch sources ─────────────────────────────────────────────────────
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}
        resp = requests.get(source["url"], headers=headers, timeout=15)
        resp.raise_for_status()
        text = clean_text(clean_html(resp.text))

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"     ✓  Fetched & saved → {len(text):,} chars")
        return {"id": source["id"], "slug": slug, "name": source["name"],
                "url": source["url"], "file": out_path, "char_count": len(text), "status": "ok"}

    except Exception as e:
        print(f"     ✗  FAILED: {e}")
        return {"id": source["id"], "slug": slug, "name": source["name"],
                "url": source["url"], "file": None, "char_count": 0, "status": f"error: {e}"}


def main():
    print("=" * 60)
    print("MIT Unofficial Guide — Document Ingestion (ingest.py)")
    print("=" * 60)

    manifest = []
    for source in SOURCES:
        entry = ingest_source(source)
        manifest.append(entry)
        if not source.get("manual"):
            time.sleep(1.0)

    manifest_path = os.path.join(RAW_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    ok      = [e for e in manifest if e["status"] == "ok"]
    manual  = [e for e in manifest if e["status"] == "needs_manual_copy"]
    failed  = [e for e in manifest if e["status"].startswith("error")]

    print("\n" + "=" * 60)
    print(f"STATUS: {len(ok)} ok | {len(manual)} need manual copy | {len(failed)} errors")

    if manual:
        print(f"\n── Still need manual copy ({len(manual)} sources) ────────────────")
        for e in manual:
            print(f"  [{e['id']:02d}] {e['name']}")
            print(f"       URL:  {e['url']}")
            print(f"       Save: data/raw/{e['slug']}.txt")
        print("\n  HOW TO: Open each URL in your browser, select the article text,")
        print("  copy it, and paste into the .txt file. Nav/header text is OK —")
        print("  the cleaner will strip it. Then re-run  python ingest.py")

    if failed:
        print(f"\n── Errors ({len(failed)}) ───────────────────────────────────────────")
        for e in failed:
            print(f"  [{e['id']:02d}] {e['name']}: {e['status']}")

    print(f"\nManifest → {manifest_path}")
    if not manual and not failed:
        print("All sources ready. Run:  python chunk.py")


if __name__ == "__main__":
    main()
