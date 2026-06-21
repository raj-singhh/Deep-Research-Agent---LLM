# Deep Research Agent

A simple Python agent project for researching topics using web search, scraping, and LLM-powered summarization.

## Files

- `pipeline.py` — orchestrates the research workflow.
- `agents.py` — builds search/reader agents and writer/critic chains.
- `tools.py` — defines web search and scraping tools.
- `requirements.txt` — Python dependencies.
- `streamlit_app.py` — optional Streamlit UI entrypoint.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with API keys, for example:
   ```env
   GROQ_API_KEY=your_api_key_here
   TAVILY_API_KEY=your_api_key_here
   ```

## Usage

Run the research pipeline:

```bash
python pipeline.py
```

Or launch the Streamlit app:

```bash
streamlit run streamlit_app.py
```

## Notes

- Add `LLM_MODEL` to `.env` if you want to override the default model name.
- The project is designed for Groq/OpenAI-compatible endpoints.
