# The Unofficial Guide — MIT Student Life RAG System

---

## Domain

This system covers everyday practical knowledge for MIT students: dining hall options, cook-for-yourself dorm life, nearby grocery stores, food assistance resources, campus transportation discounts, and general survival tips for navigating life at MIT.

While MIT provides official resources, the most actionable advice — which grocery store is actually worth the walk, which dorms have the best kitchen access, how to use the free grocery shuttles, what to do if you can't afford food — lives in scattered student blogs, Reddit threads, and informal guides that are hard to search efficiently. A student asking "where should I grocery shop near MIT?" would have to visit Rate My Professors, the MIT Admissions blog, OGE's resource page, and multiple Reddit threads to piece together an answer. This system makes that knowledge queryable in plain language and returns grounded, cited answers drawn from real documents.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | MIT Food Resource Guide (UAC) | Official resource page | https://advising.mit.edu/fli/resources/food-resource-guide/ |
| 2 | MIT Free & Low-Cost Student Resources (OGE) | Official resource page | https://oge.mit.edu/student-support-development/free-low-cost-student-resources |
| 3 | MIT Grocery Shuttle Schedule | Official transportation page | https://web.mit.edu/Facilities/transportation/shuttles/grocery.html |
| 4 | MIT Admissions: Dining Halls (student blog) | Student blog post | https://mitadmissions.org/blogs/entry/mit-dining-halls/ |
| 5 | MIT Admissions: Cook-for-Yourself Community | Student blog post | https://mitadmissions.org/blogs/entry/how-to-survive-in-a-cook-for-yourself-community/ |
| 6 | MIT Admissions: Groceries Guide | Student blog post (guest) | https://mitadmissions.org/blogs/entry/where-to-buy-food-mit-groceries-guide/ |
| 7 | MIT Admissions: Guide to Choosing a Dorm | Student blog post | https://mitadmissions.org/blogs/entry/how-to-not-choose-a-dorm/ |
| 8 | MIT Admissions: How Dorm Structure Shapes Social Life | Student blog post | https://mitadmissions.org/blogs/entry/how-dorm-structure-shapes-social-life/ |
| 9 | MIT Admissions: Starting Your First Year | Student blog post | https://mitadmissions.org/blogs/entry/so-youre-starting-your-first-year/ |
| 10 | MIT Admissions: Things I Wish I Knew | Student blog post | https://mitadmissions.org/blogs/entry/some-things-i-wish-i-knew-coming-in/ |
| 11 | MIT Admissions: An MIT Survival Guide | Student blog post | https://mitadmissions.org/blogs/entry/an_mit_survival_guide/ |
| 12 | MIT Admissions: Dining at MIT (overview) | Student blog post | https://mitadmissions.org/blogs/entry/dining-at-mit/ |
| 13 | MIT ISO: Food Resources for International Students | International student office page | https://iso.mit.edu/?p=293 |
| 14 | MIT News: TechMart At-Cost Grocery Store | News article | https://news.mit.edu/2018/mit-techmart-at-cost-grocery-store-pilot-opens-in-walker-memorial-0926 |
| 15 | Reddit r/mit: Incoming Freshman Wondering About Dorms | Reddit thread (manually collected) | https://www.reddit.com/r/mit/comments/1iz9648/incoming_freshman_wondering_about_dorms_at_mit/ |

---

## Chunking Strategy

**Chunk size:** 600 characters

**Overlap:** 100 characters

**Why these choices fit my documents:**
My corpus is a mix of two document types: long student blog posts (sources 4–12) with multi-paragraph advice, and structured resource pages (sources 1–3, 13–14) with short bullet-point lists. A 600-character chunk captures roughly one full paragraph or 3–5 bullet points — enough for a complete thought (e.g., a student's full opinion on a dining hall, or a complete description of one grocery store) without merging unrelated topics into the same chunk.

A smaller chunk (e.g., 200 characters) would fragment sentences mid-thought — a chunk might contain "The shuttle runs on Fridays" without the continuation "and the first and third Sundays," making neither chunk fully answerable on its own. A larger chunk (e.g., 1200 characters) would merge multiple dining hall descriptions or multiple grocery store entries into one embedding, causing it to weakly match many queries but precisely answer none.

The 100-character overlap is roughly one sentence. It ensures that a key fact at a paragraph boundary appears in both the preceding and following chunk, so at least one gets retrieved when a user asks about it.

The chunker also snaps boundaries to the nearest sentence end within a 60-character lookahead, so chunks don't cut mid-sentence.

**Final chunk count:** 276 chunks across 15 sources

**Sample chunks:**

1. **Source: MIT Admissions: Groceries Guide** (`mitadmissions_groceries_guide_001`)
   > "together a complete guide of all groceries near MIT. General Advice for Grocery Shopping Bring an empty backpack. You should always bring an empty backpack when going grocery shopping because it's much easier to carry groceries on your back than in your arms. When loading groceries into your backpack, make sure to put more durable items in first and to put fragile items on top."

2. **Source: MIT Free & Low-Cost Student Resources (OGE)** (`mit_oge_low_cost_resources_004`)
   > "a fantastic resource for budget-conscious individuals. Grocery shuttles . Free shuttles will take you to Brothers Market, Market Basket, Star Market, Trader Joe's, or Whole Foods, with several travel options during the week. Shuttles also make it easier to shop at Aldi, Cosco, and Target."

3. **Source: MIT Admissions: Dining Halls (student blog)** (`mitadmissions_dining_halls_023`)
   > "*SPECIAL* Salad Bar: ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ – Vassar wins on the salad bar. It has the largest salad bar, the most dressing options, and the most interesting options. The salad bars in other dining halls are mostly just random cut-up vegetables, which means your only option is a basic salad."

4. **Source: MIT News: TechMart At-Cost Grocery Store** (`mit_news_techmart_002`)
   > "When the Food Insecurity Solutions Working Group (FISWG) submitted their report in the spring of 2017 to Vice President and Dean for Student Life Suzy Nelson, one of its recommendations stood out: Open a low-cost grocery store on the MIT campus."

5. **Source: MIT Admissions: Things I Wish I Knew** (`mitadmissions_things_i_wish_i_knew_004`)
   > "I applied to the same company through the normal hiring portal and was rejected from every position. As much as I hate it, networking is important. Decide on a path or prepare for all the paths. I might have been applying for M.D./Ph.D. programs right now had I taken another year of organic chemistry."

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers` (runs locally, no API key required)

This model was chosen because it runs entirely locally with no rate limits or API costs, has fast inference (~276 chunks embedded in under 10 seconds), and performs well on short-to-medium English text. Its 256-token input limit fits comfortably within my 600-character chunk size (roughly 120–150 tokens per chunk).

**Production tradeoff reflection:**
If deploying for real users with no cost constraint, I would weigh several factors:

- **Context length**: `all-MiniLM-L6-v2` has a hard 256-token limit. If chunk sizes grew (e.g., to handle longer FAQ-style documents), it would silently truncate input. A model like `text-embedding-3-large` (OpenAI) or `voyage-large-2` supports up to 8,192 tokens, which matters for longer passages.
- **Domain specificity**: General-purpose models may underperform on MIT-specific terminology (dorm names like "EC," "Maseeh," "Random Hall," "FSILG"). A larger model or one fine-tuned on university content would embed these terms more meaningfully and improve retrieval on dorm-specific queries.
- **Latency vs. accuracy**: Local models have near-zero inference latency but lower accuracy than large API-hosted models. For a production student tool with real query volume, the accuracy tradeoff likely favors `text-embedding-3-small` (OpenAI), which balances cost and quality.
- **Multilingual support**: MIT enrolls many international students. `all-MiniLM-L6-v2` performs poorly on non-English queries. A model like `multilingual-e5-large` or `paraphrase-multilingual-MiniLM-L12-v2` would handle queries in other languages, which MiniLM does not do well.

**Retrieval test results:**

Query 1: "What grocery stores near MIT does the student grocery guide recommend for produce and bulk grains?"
- Top chunk (distance=0.3002): MIT Admissions: Groceries Guide — contains direct comparison of HMart and Harvest Co-op for produce prices. Relevant because it directly names the stores and their produce/bulk grain strengths.
- Second chunk (distance=0.3557): MIT ISO: Food Resources — lists grocery stores with walking distances. Relevant because it confirms store locations near campus.

Query 2: "Does MIT offer free grocery shuttles, and which stores do they go to?"
- Top chunk (distance=0.3097): MIT Admissions: Groceries Guide — mentions free campus shuttles and specific stores. Relevant because it gives the student perspective on shuttle use.
- Second chunk (distance=0.3217): MIT Free & Low-Cost Student Resources (OGE) — directly lists shuttle destinations. Relevant because it is the official source for shuttle information.

Query 3: "What MBTA discount is available to MIT students, and how much does it save?"
- Top chunk (distance=0.3636): MIT Free & Low-Cost Student Resources (OGE) — mentions MIT subsidizes MBTA passes. Relevant because it is the primary source for student discount information.
- Third chunk (distance=0.4205): MIT Admissions: Cook-for-Yourself — mentions 50% MBTA discount in the context of grocery shopping advice. Relevant because it confirms the discount from a student perspective.

---

## Grounded Generation

**System prompt grounding instruction:**

The system prompt explicitly restricts the LLM to the retrieved context only:

```
You are a helpful assistant for MIT students. You answer questions using ONLY the
information provided in the context documents below.

Rules you must follow:
1. Answer ONLY from the provided context. Do not use outside knowledge.
2. If the context does not contain enough information to answer the question,
   respond with exactly: "I don't have enough information in my documents to
   answer that question."
3. Be specific and cite facts directly from the context.
4. Do not speculate, infer, or add information not present in the context.
5. Keep answers concise and practical — students want actionable information.
```

Each retrieved chunk is passed to the model formatted as a numbered document block:
```
[Document 1: MIT Admissions: Groceries Guide]
<chunk text>

---

[Document 2: MIT Free & Low-Cost Student Resources (OGE)]
<chunk text>
```

**How source attribution is surfaced in the response:**

Source attribution is **programmatically guaranteed** — it is not left to the LLM to add. After the LLM generates its answer, `query.py` iterates over the retrieved chunks, deduplicates by source name, and appends each unique source as `"Source Name — URL"`. This means every response displays its sources regardless of whether the LLM mentioned them or not. The Gradio interface shows sources in a separate "Retrieved from" panel below the answer.

**Example grounded response (Query 1):**
> "According to Document 5: MIT Admissions: Groceries Guide, the student recommends HMart for 'Reasonable prices for produce' and Harvest Co-Op for 'Reasonable prices for produce' and 'bulk bins for grains and spices'."
> Sources: MIT Admissions: Groceries Guide, MIT ISO: Food Resources, MIT News: TechMart

**Example out-of-scope refusal (Times Square pizza):**
> "I don't have enough information in my documents to answer that question."
> All retrieved distances were above 0.54, confirming no relevant content existed in the corpus.

---

## Query Interface

The interface is a Gradio web UI launched with `python app.py`, accessible at `http://localhost:7860`.

**Input fields:**
- A text box labeled "Your question" where the user types a natural language query. The Enter key also submits.
- Six pre-loaded example question buttons that populate the input box on click.

**Output fields:**
- "Answer" — a multi-line text box showing the LLM's grounded response (8 lines).
- "Retrieved from" — a text box listing the deduplicated source documents with URLs (6 lines).
- "Retrieved chunks (debug view)" — a collapsible accordion showing all 5 retrieved chunks with their cosine distance scores, chunk IDs, and 150-character previews.

**Sample interaction transcript:**

```
User input: "What grocery stores near MIT are good for produce and bulk grains?"

Answer:
According to Document 5: MIT Admissions: Groceries Guide, the student recommends
HMart for "Reasonable prices for produce" and Harvest Co-Op for "Reasonable prices
for produce" and "bulk bins for grains and spices".

Retrieved from:
• MIT Admissions: Groceries Guide — https://mitadmissions.org/blogs/entry/where-to-buy-food-mit-groceries-guide/
• MIT ISO: Food Resources for International Students — https://iso.mit.edu/?p=293
• MIT News: TechMart At-Cost Grocery Store — https://news.mit.edu/2018/...
```

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What grocery stores near MIT does the student grocery guide recommend for produce and bulk grains? | HMart (produce) and Harvest Co-op (bulk grains/spices), from source 6 | Correctly named HMart for produce and Harvest Co-op for bulk bins; cited the Groceries Guide directly | Relevant (top distance: 0.30) | Accurate |
| 2 | Does MIT offer free grocery shuttles, and which stores do they go to? | Yes — Costco/Target/Aldi, Trader Joe's/Whole Foods, Market Basket/Star Market, from source 3 | Confirmed free shuttles exist; named Brothers Market, Market Basket, Star Market, Trader Joe's, Whole Foods, Costco, Target; noted scheduled times may be inaccurate | Relevant (top distance: 0.31) | Accurate |
| 3 | What do students say about the tradeoffs of living in a dining hall dorm vs a cook-for-yourself dorm freshman year? | Dining hall dorms require expensive minimum meal plans; cook-for-yourself dorms allow social bonding around cooking but require more effort, from sources 5, 7, 12 | Returned "I don't have enough information" — retrieved chunks contained relevant dorm comparison content (distances 0.26–0.32) but the grounding prompt judged the information insufficient for a direct comparison answer | Relevant (top distance: 0.26) | Inaccurate |
| 4 | What food assistance resources are available to MIT students who are struggling to afford food? | MIT S3 food pantry, TechMart at-cost store, ARM Coalition, GradSupport, from sources 1, 2, 14 | Mentioned DoingWell food swipes, MindHandHeart Student Cookbook, and Campus Food Map from the UAC guide; missed TechMart and ARM Coalition which were in other chunks not retrieved | Partially relevant (top distance: 0.29) | Partially accurate |
| 5 | What MBTA discount is available to MIT students, and how much does it save? | MIT subsidizes 50–70% of monthly MBTA pass costs, from source 2 | Correctly stated 50% discount from one source and 50–70% from another; synthesized both into a single accurate answer | Relevant (top distance: 0.36) | Accurate |

---

## Failure Case Analysis

**Question that failed:** "What do students say about the tradeoffs of living in a dining hall dorm vs a cook-for-yourself dorm freshman year?"

**What the system returned:** "I don't have enough information in my documents to answer that question."

**Root cause (tied to a specific pipeline stage):**
This is a generation-stage failure caused by the interaction between chunking and the grounding prompt. The retrieval stage actually performed well — the top chunk (distance=0.26) came from the Cook-for-Yourself Community post, which contains relevant comparison language. However, the specific tradeoff information is spread across *multiple chunks from multiple documents*: the cost argument is in `mitadmissions_choosing_dorm`, the social bonding argument is in `mitadmissions_cook_for_yourself`, and the meal plan requirement details are in `mitadmissions_dining_overview`. No single retrieved chunk contains a direct side-by-side comparison. When the LLM received five chunks each containing a piece of the answer, the strict grounding prompt ("do not speculate or infer beyond the context") caused it to judge the fragmented context as insufficient and refuse to answer, even though a human reading those same chunks could synthesize the answer.

**What I would change to fix it:**
Two targeted changes would address this. First, increase `TOP_K` from 5 to 7 or 8 for complex comparison questions, so the LLM receives more context to synthesize from. Second, soften the grounding instruction slightly for synthesis tasks: instead of "if the documents don't contain enough information, say so," use "if the documents contain partial information, synthesize what is available and note which aspects are not covered." This preserves grounding while allowing the model to draw on multiple chunks together rather than treating each as a standalone source.

---

## Spec Reflection

**One way the spec helped during implementation:**
Writing the evaluation plan in `planning.md` before building anything forced me to pick specific, verifiable questions with known answers traceable to specific source documents. This paid off directly in Milestone 4 — when testing retrieval, I already knew which source each query *should* return, so I could immediately tell when retrieval was wrong (e.g., a shuttle query returning dorm social life content) versus right. Without the evaluation plan written upfront, I would have had no baseline to judge retrieval quality against.

**One way implementation diverged from the spec:**
The spec assumed all 15 sources could be fetched automatically via `requests` + BeautifulSoup. In practice, `mitadmissions.org` returns a 403 for all non-browser requests ("Host not in allowlist"), and Reddit blocks the JSON API with a 403 as well. This required manually copying text from 11 sources into `.txt` files rather than scraping them programmatically. I updated `ingest.py` to detect pre-existing manual files and clean them on load, rather than failing silently as the original script did. The spec explicitly anticipated this scenario ("you may need to copy text manually"), so the divergence was in implementation detail rather than design principle.

---

## AI Usage

**Instance 1 — Ingestion and chunking pipeline**

- *What I gave the AI:* My `planning.md` Documents table (all 15 sources with URLs and types), my Chunking Strategy section (600-char chunks, 100-char overlap, sentence-boundary snapping), and the ingestion requirements from the project spec (fetch URLs, strip HTML/nav/boilerplate, save to `data/raw/`).
- *What it produced:* `ingest.py` using `requests` + `BeautifulSoup`, and `chunk.py` with a sliding window chunker. The ingestion script initially removed `<main>` and `<article>` tags too aggressively, causing MIT Admissions blog posts to return 0 characters because their content lives inside those tags on a JavaScript-rendered page.
- *What I changed or overrode:* The 0-character output revealed that `mitadmissions.org` blocks non-browser requests entirely (403 error), which the AI-generated code didn't handle. I directed the AI to add a `manual` flag to the source list and a file-detection fallback: if a `.txt` file already exists for a source, load and clean it instead of fetching. I also added explicit `flush=True` to all print statements after discovering the script produced no output on my terminal due to Python's output buffering on macOS.

**Instance 2 — Embedding, retrieval, and Gradio interface**

- *What I gave the AI:* My Retrieval Approach section (all-MiniLM-L6-v2, top-k=5, ChromaDB), my pipeline architecture diagram, and the grounding requirement (answer only from retrieved context, refuse if not covered, programmatic source attribution).
- *What it produced:* `embed.py` with ChromaDB `PersistentClient`, batch embedding, and a `retrieve()` function; `query.py` with the grounding system prompt and `ask()` function; `app.py` with a Gradio `Blocks` interface including example question buttons and a debug chunk viewer.
- *What I changed or overrode:* The initial `app.py` passed `theme=gr.themes.Soft()` to `gr.Blocks()`, which Gradio 6.0 moved to `launch()` — this produced a `UserWarning` on every run. I moved the theme parameter to `demo.launch(theme=gr.themes.Soft())`. I also reviewed the system prompt carefully and kept it as-is after confirming the out-of-scope test ("best pizza in Times Square") correctly returned a refusal with all chunk distances above 0.54, validating that the grounding instruction was working.
