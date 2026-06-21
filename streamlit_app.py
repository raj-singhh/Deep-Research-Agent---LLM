"""
Streamlit UI for the multi-agent deep research pipeline.

Run with:
    streamlit run streamlit_app.py

Requires pipeline.py, agents.py, tools.py in the same directory,
plus your .env with GROQ_API_KEY and TAVILY_API_KEY.
"""

import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🔎",
    layout="wide",
)

STEPS = [
    ("search", "🔍 Search", "Search agent is finding sources..."),
    ("reader", "📖 Read", "Reader agent is scraping the top result..."),
    ("writer", "✍️ Write", "Writer is drafting the report..."),
    ("critic", "🧐 Critique", "Critic is reviewing the report..."),
]

if "result" not in st.session_state:
    st.session_state.result = None
if "running" not in st.session_state:
    st.session_state.running = False

st.title("🔎 Deep Research Agent")
st.caption("Search → Read → Write → Critique, powered by a multi-agent pipeline.")

with st.sidebar:
    st.header("About")
    st.markdown(
        "This UI runs your `pipeline.py` end to end:\n\n"
        "1. **Search agent** — finds sources via Tavily\n"
        "2. **Reader agent** — scrapes the top URL\n"
        "3. **Writer chain** — drafts a structured report\n"
        "4. **Critic chain** — scores and reviews the report"
    )
    st.divider()
    st.markdown(
        "⚠️ **Heads up:** `scrape_url` in `tools.py` currently truncates "
        "scraped content to **300 characters**. This likely starves the "
        "writer of real detail — consider raising that limit "
        "(e.g. `[:5000]`) for noticeably better reports."
    )

topic = st.text_input(
    "Research topic",
    placeholder="e.g. The impact of AI on renewable energy grid management",
)

run_clicked = st.button("Run research", type="primary", disabled=st.session_state.running)

step_placeholders = {}
status_row = st.container()

if run_clicked:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        st.session_state.running = True
        st.session_state.result = None

        # live progress UI
        cols = status_row.columns(len(STEPS))
        for (key, label, _), col in zip(STEPS, cols):
            with col:
                step_placeholders[key] = st.empty()
                step_placeholders[key].info(f"⏳ {label}\n\nWaiting...")

        output_area = st.container()
        step_outputs = {}

        def on_step(step_name, status, payload):
            label = dict((k, l) for k, l, _ in STEPS)[step_name]
            if status == "start":
                msg = dict((s[0], s[2]) for s in STEPS)[step_name]
                step_placeholders[step_name].info(f"⏳ {label}\n\n{msg}")
            elif status == "done":
                step_placeholders[step_name].success(f"✅ {label}\n\nDone")
                step_outputs[step_name] = payload
                with output_area:
                    with st.expander(f"{label} — output", expanded=(step_name == "critic")):
                        st.markdown(payload if payload else "_(empty)_")
            elif status == "error":
                step_placeholders[step_name].error(f"❌ {label}\n\nFailed")
                with output_area:
                    st.error(f"**{label} failed:**\n\n{payload}")

        try:
            with st.spinner("Running pipeline..."):
                result = run_research_pipeline(topic, on_step=on_step)
            st.session_state.result = result
        except Exception as e:
            st.error(f"Pipeline crashed unexpectedly: {e}")
        finally:
            st.session_state.running = False

# Final results section (persists across reruns)
if st.session_state.result and "error" not in st.session_state.result:
    result = st.session_state.result
    st.divider()
    st.header("📄 Final Report")
    st.markdown(result.get("report", "_No report generated._"))

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇️ Download report (.md)",
            data=result.get("report", ""),
            file_name="research_report.md",
            mime="text/markdown",
        )
    with col2:
        st.download_button(
            "⬇️ Download report (.txt)",
            data=result.get("report", ""),
            file_name="research_report.txt",
            mime="text/plain",
        )

    st.header("🧐 Critic Feedback")
    st.markdown(result.get("feedback", "_No feedback generated._"))

    with st.expander("🔍 Raw search results"):
        st.text(result.get("search_result", ""))

    with st.expander("📖 Raw scraped content"):
        st.text(result.get("scraped_content", ""))

elif st.session_state.result and "error" in st.session_state.result:
    st.error(f"Pipeline stopped early: {st.session_state.result['error']}")