# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

---I chose the domain of "The Unofficial MIT Survival Guide." This system combines information about dining, dorm life, grocery options, food insecurity resources, campus hacks, and advice shared by MIT students. While MIT provides official resources, many of the most useful insights come from student blogs, Reddit discussions, and community-generated guides that are scattered across different places and difficult to search efficiently. This system aims to bring together both official information and student experiences into a single searchable guide that helps students navigate everyday life at MIT.

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | MIT Food Resource Guide (UAC) | Official list of food pantries, grocery resources, and food assistance for MIT students | https://advising.mit.edu/fli/resources/food-resource-guide/ |
| 2 | MIT Free & Low-Cost Student Resources (OGE) | Lists grocery shuttles, MBTA discounts, food discounts, and campus perks | https://oge.mit.edu/student-support-development/free-low-cost-student-resources |
| 3 | MIT Grocery Shuttle Schedule | Official shuttle routes and schedules to Costco, Trader Joe's, Whole Foods, Market Basket, Star Market | https://web.mit.edu/Facilities/transportation/shuttles/grocery.html |
| 4 | MIT Admissions: Dining Halls (student blog) | Student-written ranking and review of MIT dining halls | https://mitadmissions.org/blogs/entry/mit-dining-halls/ |
| 5 | MIT Admissions: How to Survive in a Cook-for-Yourself Community | Student advice on living in non-dining dorms, grocery shopping, meal prep | https://mitadmissions.org/blogs/entry/how-to-survive-in-a-cook-for-yourself-community/ |
| 6 | MIT Admissions: Groceries Guide (guest post) | Detailed student guide comparing nearby grocery stores (HMart, Star Market, Trader Joe's, Harvest Co-op, etc.) | https://mitadmissions.org/blogs/entry/where-to-buy-food-mit-groceries-guide/ |
| 7 | MIT Admissions: Guide to Choosing a Dorm | Student breakdown of dorm cultures, pricing tiers, dining hall dorms vs cook-for-yourself | https://mitadmissions.org/blogs/entry/how-to-not-choose-a-dorm/ |
| 8 | MIT Admissions: How Dorm Structure Shapes Social Life | Student perspective on how physical dorm layout affects community and daily life | https://mitadmissions.org/blogs/entry/how-dorm-structure-shapes-social-life/ |
| 9 | MIT Admissions: Starting Your First Year | Tips from a student OL — clubs, dining, first-week survival | https://mitadmissions.org/blogs/entry/so-youre-starting-your-first-year/ |
| 10 | MIT Admissions: Things I Wish I Knew | Upperclassman advice on navigating MIT academically and socially | https://mitadmissions.org/blogs/entry/some-things-i-wish-i-knew-coming-in/ |
| 11 | MIT Admissions: An MIT Survival Guide | Early but useful student tips on sleep, food, social life, and campus navigation | https://mitadmissions.org/blogs/entry/an_mit_survival_guide/ |
| 12 | MIT Admissions: Dining at MIT (overview) | Explains meal plan options, dining hall vs cook-for-yourself tradeoffs | https://mitadmissions.org/blogs/entry/dining-at-mit/ |
| 13 | MIT ISO: Food Resources for International Students | Lists grocery stores by distance from campus with walking times, food apps (Too Good To Go), on-campus options | https://iso.mit.edu/?p=293 |
| 14 | MIT News: TechMart At-Cost Grocery Store | About MIT's on-campus grocery store selling staples at cost for students | https://news.mit.edu/2018/mit-techmart-at-cost-grocery-store-pilot-opens-in-walker-memorial-0926 |
| 15 | Reddit r/mit: Incoming Freshman Wondering About Dorms | Student Q&A on dorm culture, dining, and first-year experience | https://www.reddit.com/r/mit/comments/1iz9648/incoming_freshman_wondering_about_dorms_at_mit/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 600 characters

**Overlap:** 100 characters

**Reasoning:** My documents are a mix of two types: long student blog posts (sources 4–12) with multi-paragraph
advice, and structured resource pages (sources 1–3, 13–14) with short bullet-point lists. A
600-character chunk captures roughly one full paragraph or 3–5 bullet points — enough for a
complete thought (e.g., a student's full opinion on a dining hall, or a complete description of
one grocery store) without merging unrelated topics into the same chunk.

A smaller chunk (e.g., 200 characters) would fragment sentences mid-thought — a chunk might
contain "The shuttle runs on Fridays" without the continuation "and the first and third Sundays,"
making neither chunk fully answerable on its own. A larger chunk (e.g., 1200 characters) would
merge multiple dining hall descriptions or multiple grocery store entries into one embedding,
causing it to weakly match many queries but precisely answer none.

The 100-character overlap is roughly one sentence. It ensures that a key fact at a paragraph
boundary — like a specific store name or shuttle schedule detail — appears in both the preceding
and following chunk, so at least one gets retrieved when a user asks about it.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**  all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key required)


**Top-k:** 5

**Reasoning for top-k:**
My documents cover several distinct subtopics (dining halls, grocery stores, dorm life, food
assistance, campus tips). A query about grocery shuttles should pull 5 chunks to capture the
official shuttle schedule, a student blog perspective, and the ISO resource page — all of which
may hold complementary details. Fewer than 4 risks missing a key source; more than 6 risks
flooding the LLM with loosely related content about unrelated subtopics (e.g., a question about
shuttles pulling in dorm culture content).

**Production tradeoff reflection:**
If deploying for real users with no cost constraint, I would weigh:
- **Context length**: all-MiniLM-L6-v2 has a 256-token input limit, which is fine for my
  600-character chunks but would truncate longer passages. A model like text-embedding-3-large
  (OpenAI) or voyage-large-2 supports longer inputs, which matters if chunk size grows.
- **Domain specificity**: general-purpose models may underperform on MIT-specific jargon
  (dorm names like "EC," "Maseeh," "Random Hall"). A fine-tuned or larger model would embed
  these more meaningfully.
- **Latency vs. accuracy**: local models like MiniLM have near-zero latency but lower accuracy
  than API models. For a production student tool, the accuracy tradeoff likely favors an API
  model like OpenAI's text-embedding-3-small, which balances cost and quality.
- **Multilingual support**: MIT has many international students; a model like multilingual-e5
  would handle queries in other languages, which MiniLM does not do well.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What grocery stores near MIT does the student grocery guide recommend for produce and bulk grains?|Harvest Co-op (bulk bins for grains and spices, reasonable produce prices) and the Stata Market produce stand (open Tuesdays, cash only) — from source 6 |
| 2 |Does MIT offer free grocery shuttles, and which stores do they go to? | Yes — MIT runs free shuttles to Costco/Target/Aldi (Sundays), Trader Joe's/Whole Foods (Fridays + some Sundays), and Market Basket/Star Market — from source 3|
| 3 | What do students say about the tradeoffs of living in a dining hall dorm vs. a cook-for-yourself dorm freshman year? | Dining hall dorms require a minimum meal plan (expensive, inflexible); cook-for-yourself dorms allow more social bonding around cooking but require more effort — from sources 5, 7, 12|
| 4 | What food assistance resources are available to MIT students who are struggling to afford food? | MIT S^3 food pantry, TechMart at-cost grocery store, the ARM Coalition, emergency funds through GradSupport — from sources 1, 2, 14 |
| 5 |What MBTA discount is available to MIT students, and how much does it save? |MIT subsidizes 50–70% of monthly MBTA pass costs for bus, subway, commuter rail, and commuter boat — from source 2 |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Navigation and boilerplate text surviving cleaning**: MIT Admissions blog posts contain
   author bios, comment counts, footnote markers (e.g., "⁠01"), and "Keep Reading" links
   embedded throughout the text. If cleaning doesn't strip these, chunks like "⁠01 ahahaha
   sorry" or "Keep Reading · Parting Remarks" will get embedded and may surface as false
   matches for unrelated queries. I'll need to print a sample of cleaned text from each source before chunking and verify no boilerplate remains.

2. **Key facts split across chunk boundaries**: Several documents contain information that
   spans multiple sentences across a natural break — for example, shuttle schedules that list
   the route on one line and the day/time on the next. If these split into separate chunks,
   neither chunk alone answers "when does the Trader Joe's shuttle run?" The 100-character
   overlap mitigates this, but it won't catch every case. I'll test this specifically in my
   evaluation questions.

3. **Reddit thread noise**: The Reddit source contains not just answers but also jokes,
   off-topic replies, and meta-comments about MIT admissions. These will generate chunks with
   high word count but no useful information, and they may retrieve on general MIT queries
   even when irrelevant. I may need to manually filter comments below a score threshold or
   only retain top-level comments.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

┌─────────────────────────────────────────────────────────────────┐
│                        PIPELINE OVERVIEW                        │
└─────────────────────────────────────────────────────────────────┘

1. DOCUMENT INGESTION          2. CHUNKING
   requests + BeautifulSoup  →  custom splitter
   15 URLs fetched               600-char chunks
   HTML stripped                 100-char overlap
   Saved to /data/raw/*.txt      metadata: {source, chunk_index}
          │                              │
          └──────────────────────────────┘
                                         │
                                         ▼
3. EMBEDDING + VECTOR STORE    4. RETRIEVAL
   sentence-transformers       →  ChromaDB query
   all-MiniLM-L6-v2               top-k = 5
   ChromaDB collection             returns chunks + source names
   stored locally
          │                              │
          └──────────────────────────────┘
                                         │
                                         ▼
                            5. GENERATION
                               Groq API
                               llama-3.3-70b-versatile
                               grounded prompt (context-only)
                               output: answer + sources
                                         │
                                         ▼
                            6. INTERFACE
                               Gradio web UI (app.py)
                               Input: question textbox
                               Output: answer + retrieved sources

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
Tool: Claude
Input: My Documents table (all 15 sources with URLs), my Chunking Strategy section (600-char
chunks, 100-char overlap), and the ingestion requirements from the project spec (load raw
documents, clean navigation text and HTML artifacts, produce structured text).
Expected output: A script `ingest.py` that fetches each URL using `requests` + `BeautifulSoup`,
strips nav/footer/boilerplate, and saves cleaned text to `/data/raw/` as .txt files. A second
script `chunk.py` that loads those files, splits them into 600-character chunks with 100-char
overlap, attaches source metadata (filename, chunk index), and saves chunks as a JSON list.
How I'll verify: I'll print 5 random chunks and check each is readable, self-contained, and
contains no HTML artifacts or nav text. I'll also check total chunk count is between 100–600.

**Milestone 4 — Embedding and retrieval:**
Tool: Claude
Input: My Retrieval Approach section (all-MiniLM-L6-v2, top-k=5), my Architecture diagram,
and the chunk JSON output from Milestone 3.
Expected output: A script `embed.py` that loads chunks, embeds them with
`SentenceTransformer("all-MiniLM-L6-v2")`, stores them in a ChromaDB collection with source
metadata, and exposes a `retrieve(query, k=5)` function returning chunks + source filenames.
How I'll verify: I'll run 3 of my evaluation questions through `retrieve()` and check that
returned chunks visibly relate to each question and have distance scores below 0.5.

**Milestone 5 — Generation and interface:**
Tool: Claude
Input: My grounding requirement (answer only from retrieved context, refuse if not covered),
my output format (answer + source list), and the Gradio interface requirements from the spec.
Expected output: A `query.py` with an `ask(question)` function that calls `retrieve()`, builds a prompt with retrieved chunks as context, calls Groq's llama-3.3-70b-versatile, and returns `{"answer": ..., "sources": [...]}`. Plus `app.py` with a Gradio UI wiring the input box to `ask()` and displaying answer and sources separately.
How I'll verify: I'll test all 5 evaluation questions end-to-end and confirm source attribution appears in every response. I'll also ask one out-of-scope question and confirm the system refuses rather than hallucinating.
