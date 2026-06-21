# Deep Research Agent

A Python research assistant that combines web search, page scraping, and large language models to generate structured topic reports.

## Tech Stack

- Python 3
- LangChain / LangGraph for agent orchestration
- Groq/OpenAI-compatible LLM API
- Tavily search API
- Requests + BeautifulSoup for web scraping
- Streamlit for optional UI

## Project Overview

This repository demonstrates a basic research pipeline where:
- `pipeline.py` manages the workflow
- `agents.py` configures LLM agents and prompt templates
- `tools.py` provides web search and URL scraping utilities
- `streamlit_app.py` offers an optional UI for interactive use

The current implementation uses Groq/OpenAI-compatible LLM access and a third-party search client for retrieving web results.

## Features

- Search for recent, relevant information using `web_search`
- Scrape chosen URLs with `scrape_url`
- Build a research report with a writer prompt
- Review the report with a critic prompt
- Optional Streamlit interface for easier experimentation

## Files

- `pipeline.py` — orchestrates the end-to-end research flow
- `agents.py` — creates search/reader agents and writer/critic chains
- `tools.py` — defines the web search and scrape tools
- `requirements.txt` — Python dependencies for the project
- `streamlit_app.py` — optional Streamlit UI entry point
- `.gitignore` — ignores virtual environment and temporary files
- `README.md` — this documentation

## Setup

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the repository root with your API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

## Configuration

Optional `.env` settings:

```env
LLM_MODEL=llama-3.3-70b-versatile
LLM_MAX_TOKENS=1000
LLM_TEMPERATURE=0.2
GROQ_BASE_URL=https://api.groq.com/openai/v1
```

Use a smaller model or lower `LLM_MAX_TOKENS` to reduce token usage and avoid rate limit issues.

## Usage

### Run the research pipeline

```bash
python pipeline.py
```

Follow the prompt to enter a research topic. The script will:
1. search the web
2. choose and scrape a relevant page
3. draft a research report
4. evaluate the report with a critic prompt

### Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

This is useful for exploring the toolchain through a browser-based interface.

## Troubleshooting

- `RateLimitError`: try a smaller model or lower `LLM_MAX_TOKENS`.
- missing API key: ensure `GROQ_API_KEY` and `TAVILY_API_KEY` are set in `.env`.
- `requests` scrape failures: the target site may block scraping or require a more robust parser.

## Notes

- The search and scraping tools are simple examples and may need customization for production usage.
- The writing and critic prompts are defined in `agents.py`; adjust them to change output style.
- Keep `.env` out of version control; it is ignored by `.gitignore`.
