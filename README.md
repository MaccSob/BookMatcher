# Book Matcher

A mood-based book recommendation tool. Instead of matching by genre alone, it takes a free-text description of your current reading context ("something light before bed, 30 minutes max") and returns real books — pulled from a live catalog, not invented by an LLM — with a short explanation of why each one fits.

## Why this exists

Asking an LLM directly for book recommendations works, but it's prone to hallucination: titles, authors, and page counts can be plausible-sounding but wrong. This project grounds recommendations in real data from the [Open Library API](https://openlibrary.org/developers/api), and uses an LLM only to interpret mood and rank/explain — not to invent facts. This is a retrieval-augmented generation (RAG) pattern: retrieve real candidates first, then let the LLM reason over them.

## How it works

1. **Interpret mood** — an LLM (Gemini) turns a free-text mood description into a concrete, searchable query (e.g. a genre) plus supporting themes, pace, and a page-count guideline.
2. **Search** — that query is used to search Open Library for real candidate books (title, author included).
3. **Fetch details** — for each candidate, fetch its full metadata (description, subject tags) from Open Library's works endpoint.
4. **Clean** — noisy subject tags (library catalog codes, translation labels, near-duplicates across languages) are filtered out.
5. **Rank & explain** — the LLM reviews the candidates' real descriptions and picks the best 3-5 matches for the original mood, with a short reasoning for each.
6. **Serve** — the whole pipeline is exposed as a REST API (FastAPI), with a small HTML page to try it out.

## Statusr

**Working end-to-end**, including a REST API and a minimal test frontend.

**Done:**
- Search Open Library and fetch per-book details (description, subjects, author)
- Clean noisy subject tags
- LLM mood interpretation with a concrete, searchable query
- LLM ranking and reasoning over real candidates, using structured output (Pydantic schemas) for reliable parsing
- REST API (`POST /recommend`) built with FastAPI, with CORS enabled for local frontend use
- Simple HTML/JS frontend (`index.html`) to test the API without touching `/docs`

**Planned:**
- Caching to avoid redundant API calls
- More robust error handling around missing/inconsistent Open Library metadata and slow API responses
- Option to force response language regardless of input language

## Project structure

```
book_matcher/
├── books.py      # Open Library search, detail fetching, subject cleaning
├── llm.py        # Gemini integration: mood interpretation, ranking & reasoning
├── main.py       # Ties it together: get_recommendations(mood_text)
├── api.py        # FastAPI app exposing POST /recommend
├── index.html    # Minimal frontend to test the API in a browser
├── .env          # API keys (not committed)
├── .gitignore
└── requirements.txt
```

## Tech stack

- Python
- `requests` — HTTP calls to Open Library
- `google-genai` — Gemini API client (Interactions API, structured output)
- `pydantic` — response schemas for reliable, structured LLM output
- `python-dotenv` — local API key management
- `fastapi` + `uvicorn` — REST API layer
- Plain HTML/JS — test frontend, no framework

## Data source

[Open Library API](https://openlibrary.org/developers/api) — free, no API key required. Please note their guidance on caching and setting a descriptive User-Agent to avoid unnecessary load on their (non-profit) service.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file with your Gemini API key:
```
GEMINI_API_KEY=your_key_here
```

## Running the API

```bash
uvicorn api:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

Example request:
```bash
curl -X POST http://127.0.0.1:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"mood": "something light before bed, 30 minutes max"}'
```

Example response:
```json
[
  {
    "title": "Lovestruck",
    "author": "Simone Kelly",
    "reasoning": "A lighthearted romantic comedy that's easy to pick up and put down before sleep."
  }
]
```

## Using the test frontend

With the API running, open `index.html` directly in a browser (double-click it — no server needed). Type a mood, click the button, and see recommendations rendered with title, author, and reasoning.

## License

TBD
