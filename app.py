"""
app.py — Milestone 5: Gradio Web Interface
Runs the MIT Unofficial Guide RAG system as a web UI.

Usage:
    python app.py
    Then open: http://localhost:7860
"""

import gradio as gr
from query import ask

# ── Suggested example questions (shown in the UI) ─────────────────────────────
EXAMPLES = [
    "Does MIT offer free grocery shuttles, and which stores do they go to?",
    "What grocery stores near MIT are good for produce and bulk grains?",
    "What are the tradeoffs of living in a dining hall dorm vs cook-for-yourself?",
    "What food assistance resources are available to MIT students who can't afford food?",
    "What MBTA discount is available to MIT students?",
    "What do students say about Maseeh dining hall?",
]


def handle_query(question: str):
    """Called by Gradio on every button click or Enter press."""
    if not question.strip():
        return "Please enter a question.", "", ""

    result = ask(question)

    answer = result["answer"]

    # Format sources as a readable list
    if result["sources"]:
        sources_text = "\n".join(f"• {s}" for s in result["sources"])
    else:
        sources_text = "No sources retrieved."

    # Format chunk details for the debug panel
    chunk_lines = []
    for c in result["chunks"]:
        chunk_lines.append(
            f"[{c['distance']:.4f}] {c['source_name']}\n"
            f"  {c['text'][:150].replace(chr(10), ' ')}..."
        )
    chunks_text = "\n\n".join(chunk_lines)

    return answer, sources_text, chunks_text


# ── Build Gradio UI ───────────────────────────────────────────────────────────
# with gr.Blocks(title="MIT Unofficial Guide", theme=gr.themes.Soft()) as demo:
with gr.Blocks(title="MIT Unofficial Guide") as demo:

    gr.Markdown("""
    # 🎓 The MIT Unofficial Guide
    **Ask questions about MIT student life — dining, groceries, dorms, food resources, and campus tips.**
    Answers are grounded in real MIT student blogs, official resources, and community guides.
    """)

    with gr.Row():
        with gr.Column(scale=3):
            question_box = gr.Textbox(
                label="Your question",
                placeholder="e.g. What grocery stores are near MIT campus?",
                lines=2,
            )
            ask_btn = gr.Button("Ask", variant="primary")

        with gr.Column(scale=1):
            gr.Markdown("**Example questions:**")
            for ex in EXAMPLES:
                gr.Button(ex, size="sm").click(
                    fn=lambda q=ex: q,
                    outputs=question_box,
                )

    gr.Markdown("---")

    with gr.Row():
        with gr.Column(scale=2):
            answer_box = gr.Textbox(
                label="Answer",
                lines=10,
                interactive=False,
            )
        with gr.Column(scale=1):
            sources_box = gr.Textbox(
                label="Retrieved from",
                lines=6,
                interactive=False,
            )

    with gr.Accordion("Retrieved chunks (debug view)", open=False):
        chunks_box = gr.Textbox(
            label="Top-5 chunks with distance scores",
            lines=12,
            interactive=False,
        )

    # Wire up button and Enter key
    ask_btn.click(
        fn=handle_query,
        inputs=question_box,
        outputs=[answer_box, sources_box, chunks_box],
    )
    question_box.submit(
        fn=handle_query,
        inputs=question_box,
        outputs=[answer_box, sources_box, chunks_box],
    )

    gr.Markdown("""
    ---
    *Answers are drawn only from collected documents. Sources are listed for every response.*
    """)


if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
