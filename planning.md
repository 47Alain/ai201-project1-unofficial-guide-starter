# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

--- I chose the domain of MIT food, dining, and student food resources. This knowledge is valuable because students frequently have questions about meal plans, dining halls, cook-for-yourself dorms, grocery options, and food support resources. While some of this information exists on official MIT websites, students often have to piece it together from blogs, reports, FAQs, and discussion threads. This system makes these scattered resources searchable through a single interface.

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | MIT Dining | Official dining information and meal plans | https://studentlife.mit.edu/dining/ |
| 2 | MIT Student Life | Overview of student dining resources | https://studentlife.mit.edu/ |
| 3 | MIT Food Resource Guide | Grocery stores and food resources near MIT | https://advising.mit.edu/fli/resources/food-resource-guide/ |
| 4 | DoingWell Food Resources | Food and financial assistance programs | https://doingwell.mit.edu/foodandfinancial/ |
| 5 | Food @ MIT Guide | Student-curated food resource links | https://linktr.ee/food.at.mit |
| 6 | MIT UA Food Report | Student perspectives on food insecurity and dining | https://ua-edit.squarespace.com/s/Food-Report-Final.pdf |
| 7 | MIT Admissions Blog | "How to Survive in a Cook-for-Yourself Community" | https://mitadmissions.org/blogs/entry/how-to-survive-in-a-cook-for-yourself-community/ |
| 8 | MIT Admissions Blog | "MIT Dining Halls" | https://mitadmissions.org/blogs/entry/mit-dining-halls/ |
| 9 | MIT Admissions FAQ | Housing and dining FAQ | https://mitadmissions.org/help/faq/housing-dining/ |
| 10 | Reddit r/mit | Student discussion about dorms and meal plans | https://www.reddit.com/r/mit/comments/1iz9648/incoming_freshman_wondering_about_dorms_at_mit/ |

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
