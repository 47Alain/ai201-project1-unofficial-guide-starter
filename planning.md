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

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
