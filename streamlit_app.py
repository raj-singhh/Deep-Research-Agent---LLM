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
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Design system
# ---------------------------------------------------------------------------
# Palette: ink background, paper text, single brass/amber accent.
# Type: Source Serif 4 for headings & report body (this is a research desk,
# not a SaaS dashboard); JetBrains Mono for status/meta/labels, since the
# pipeline genuinely behaves like a running process with logs.

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --ink: #0F1115;
    --panel: #171A21;
    --panel-line: #2A2E38;
    --paper: #EDE9E0;
    --paper-dim: #9CA0AC;
    --brass: #D4A24E;
    --brass-dim: #8A6B35;
    --ok: #6FAE8C;
    --err: #C2645A;
}

html, body, [class*="css"] {
    font-family: 'Source Serif 4', Georgia, serif;
}

.stApp {
    background: var(--ink);
    color: var(--paper);
}

#MainMenu, header[data-testid="stHeader"], footer {
    background: transparent;
}

section[data-testid="stSidebar"] {
    background: var(--panel);
    border-right: 1px solid var(--panel-line);
}

/* ---------- Masthead ---------- */
.masthead {
    border-bottom: 1px solid var(--panel-line);
    padding-bottom: 22px;
    margin-bottom: 8px;
}
.masthead .eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--brass);
    margin-bottom: 6px;
}
.masthead h1 {
    font-family: 'Source Serif 4', serif;
    font-weight: 700;
    font-size: 42px;
    letter-spacing: -0.01em;
    color: var(--paper);
    margin: 0;
    line-height: 1.1;
}
.masthead .sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--paper-dim);
    margin-top: 10px;
}

/* ---------- Input row ---------- */
div[data-testid="stTextInput"] input {
    background: var(--panel);
    border: 1px solid var(--panel-line);
    color: var(--paper);
    font-family: 'Source Serif 4', serif;
    font-size: 17px;
    padding: 14px 16px;
    border-radius: 2px;
}
div[data-testid="stTextInput"] input:focus {
    border-color: var(--brass);
    box-shadow: 0 0 0 1px var(--brass);
}
div[data-testid="stTextInput"] label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--paper-dim);
}

.stButton button {
    background: var(--brass);
    color: var(--ink);
    border: none;
    border-radius: 2px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 12px 28px;
    transition: background 0.15s ease;
}
.stButton button:hover {
    background: #E6B563;
    color: var(--ink);
}
.stButton button:disabled {
    background: var(--panel-line);
    color: var(--paper-dim);
}

/* ---------- Pipeline rail ---------- */
.rail {
    display: flex;
    flex-direction: column;
    margin: 28px 0 8px 0;
}
.rail-step {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 14px 0;
    border-bottom: 1px solid var(--panel-line);
}
.rail-step:last-child { border-bottom: none; }

.rail-marker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    width: 30px;
    height: 30px;
    min-width: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--panel-line);
    color: var(--paper-dim);
}
.rail-marker.pending { color: var(--paper-dim); border-color: var(--panel-line); }
.rail-marker.active {
    color: var(--ink);
    background: var(--brass);
    border-color: var(--brass);
}
.rail-marker.done { color: var(--ok); border-color: var(--ok); }
.rail-marker.error { color: var(--err); border-color: var(--err); }

.rail-body { flex: 1; }
.rail-title {
    font-family: 'Source Serif 4', serif;
    font-weight: 600;
    font-size: 17px;
    color: var(--paper);
}
.rail-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.04em;
    margin-top: 3px;
}
.rail-status.pending { color: var(--paper-dim); }
.rail-status.active { color: var(--brass); }
.rail-status.done { color: var(--ok); }
.rail-status.error { color: var(--err); }

/* ---------- Section labels ---------- */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--brass);
    border-bottom: 1px solid var(--panel-line);
    padding-bottom: 10px;
    margin: 36px 0 18px 0;
}

/* ---------- Report panel ---------- */
.report-panel {
    background: var(--panel);
    border: 1px solid var(--panel-line);
    border-left: 3px solid var(--brass);
    padding: 32px 36px;
    border-radius: 2px;
    font-family: 'Source Serif 4', serif;
    font-size: 16px;
    line-height: 1.7;
    color: var(--paper);
}
.report-panel h1, .report-panel h2, .report-panel h3 {
    font-family: 'Source Serif 4', serif;
    color: var(--paper);
}

.feedback-panel {
    background: var(--panel);
    border: 1px solid var(--panel-line);
    border-left: 3px solid var(--ok);
    padding: 28px 32px;
    border-radius: 2px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    line-height: 1.8;
    color: var(--paper);
    white-space: pre-wrap;
}

/* ---------- Expanders as raw-log panels ---------- */
div[data-testid="stExpander"] {
    background: var(--panel);
    border: 1px solid var(--panel-line);
    border-radius: 2px;
}
div[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: var(--paper-dim);
}

/* ---------- Download buttons ---------- */
div[data-testid="stDownloadButton"] button {
    background: transparent;
    border: 1px solid var(--brass-dim);
    color: var(--brass);
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.05em;
    border-radius: 2px;
}
div[data-testid="stDownloadButton"] button:hover {
    border-color: var(--brass);
    background: rgba(212, 162, 78, 0.08);
}

/* ---------- Misc ---------- */
.stAlert { border-radius: 2px; font-family: 'JetBrains Mono', monospace; font-size: 13px; }
hr { border-color: var(--panel-line); }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Pipeline stage definitions
# ---------------------------------------------------------------------------
STEPS = [
    ("search", "01", "Search", "Querying sources for recent, reliable coverage."),
    ("reader", "02", "Read", "Scraping the most relevant result for depth."),
    ("writer", "03", "Write", "Drafting a structured report from gathered research."),
    ("critic", "04", "Critique", "Scoring the report and noting gaps."),
]

if "result" not in st.session_state:
    st.session_state.result = None
if "running" not in st.session_state:
    st.session_state.running = False
if "step_status" not in st.session_state:
    st.session_state.step_status = {k: "pending" for k, *_ in STEPS}
if "step_output" not in st.session_state:
    st.session_state.step_output = {}

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        "<div style='font-family:JetBrains Mono;font-size:12px;"
        "letter-spacing:0.14em;text-transform:uppercase;color:#D4A24E;"
        "margin-bottom:10px;'>Pipeline</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='font-family:Source Serif 4;font-size:14.5px;"
        "line-height:1.7;color:#EDE9E0;'>"
        "A topic moves through four agents in sequence — search, read, "
        "write, critique — each handing its output to the next."
        "</div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Masthead
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="masthead">'
    '<div class="eyebrow">Multi-Agent Research System</div>'
    '<h1>Deep Research Agent</h1>'
    '<div class="sub">SEARCH &rarr; READ &rarr; WRITE &rarr; CRITIQUE</div>'
    '</div>',
    unsafe_allow_html=True,
)

topic = st.text_input(
    "Research topic",
    placeholder="e.g. The impact of AI on renewable energy grid management",
    label_visibility="visible",
)

run_clicked = st.button(
    "Run research" if not st.session_state.running else "Running…",
    disabled=st.session_state.running,
)

# ---------------------------------------------------------------------------
# Pipeline rail renderer
# ---------------------------------------------------------------------------
rail_placeholder = st.empty()


def render_rail(status_map):
    parts = ['<div class="rail">']
    for key, num, title, _ in STEPS:
        status = status_map.get(key, "pending")
        marker_icon = {"pending": num, "active": "…", "done": "✓", "error": "✕"}[status]
        status_text = {
            "pending": "waiting",
            "active": "in progress",
            "done": "complete",
            "error": "failed",
        }[status]
        # IMPORTANT: no leading whitespace / newlines between tags.
        # Streamlit's markdown renderer parses indented or blank-line-
        # separated content as markdown, which breaks out of raw-HTML
        # mode partway through a multi-block string. Keep every step
        # as one unbroken line.
        parts.append(
            f'<div class="rail-step">'
            f'<div class="rail-marker {status}">{marker_icon}</div>'
            f'<div class="rail-body">'
            f'<div class="rail-title">{title}</div>'
            f'<div class="rail-status {status}">{status_text}</div>'
            f'</div>'
            f'</div>'
        )
    parts.append("</div>")
    rail_placeholder.markdown("".join(parts), unsafe_allow_html=True)


render_rail(st.session_state.step_status)

output_area = st.container()

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if run_clicked:
    if not topic.strip():
        st.warning("Enter a topic before running.")
    else:
        st.session_state.running = True
        st.session_state.result = None
        st.session_state.step_status = {k: "pending" for k, *_ in STEPS}
        st.session_state.step_output = {}
        render_rail(st.session_state.step_status)

        def on_step(step_name, status, payload):
            if status == "start":
                st.session_state.step_status[step_name] = "active"
            elif status == "done":
                st.session_state.step_status[step_name] = "done"
                st.session_state.step_output[step_name] = payload
            elif status == "error":
                st.session_state.step_status[step_name] = "error"
                st.session_state.step_output[step_name] = payload
            render_rail(st.session_state.step_status)

        try:
            result = run_research_pipeline(topic, on_step=on_step)
            st.session_state.result = result
        except Exception as e:
            st.error(f"Pipeline crashed unexpectedly: {e}")
        finally:
            st.session_state.running = False

# ---------------------------------------------------------------------------
# Per-step raw output (collapsed logs)
# ---------------------------------------------------------------------------
if st.session_state.step_output:
    with output_area:
        st.markdown('<div class="section-label">Stage Output</div>', unsafe_allow_html=True)
        for key, _, title, _ in STEPS:
            if key in st.session_state.step_output:
                is_error = st.session_state.step_status.get(key) == "error"
                with st.expander(f"{title} {'— failed' if is_error else ''}", expanded=is_error):
                    if is_error:
                        st.error(st.session_state.step_output[key])
                    else:
                        st.text(st.session_state.step_output[key])

# ---------------------------------------------------------------------------
# Final results
# ---------------------------------------------------------------------------
result = st.session_state.result

if result and "error" not in result:
    st.markdown('<div class="section-label">Final Report</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="report-panel">{result.get("report", "")}</div>', unsafe_allow_html=True)

    col1, col2, _ = st.columns([1, 1, 4])
    with col1:
        st.download_button(
            "↓ Download .md",
            data=result.get("report", ""),
            file_name="research_report.md",
            mime="text/markdown",
        )
    with col2:
        st.download_button(
            "↓ Download .txt",
            data=result.get("report", ""),
            file_name="research_report.txt",
            mime="text/plain",
        )

    st.markdown('<div class="section-label">Critic Feedback</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="feedback-panel">{result.get("feedback", "")}</div>', unsafe_allow_html=True)

elif result and "error" in result:
    st.markdown('<div class="section-label">Run Failed</div>', unsafe_allow_html=True)
    st.error(result["error"])