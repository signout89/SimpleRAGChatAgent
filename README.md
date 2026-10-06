# Simple RAG Chat Agent

A chat assistant that answers questions about Insurellm, a fictional insurance tech company, using retrieval-augmented generation over the Markdown files in `knowledge-base/`.

## How it works

- `ingest.py` splits each document into chunks with an LLM, embeds them with `text-embedding-3-large`, and stores them in a local Chroma database (`preprocessed_db/`).
- `answer.py` rewrites the question, retrieves matching chunks, reranks them, and answers with `gpt-4.1-mini`.
- `main.py` serves a Gradio chat UI that shows the answer and the retrieved context.

## Requirements

- Python 3.14+ and [uv](https://docs.astral.sh/uv/)
- An OpenAI API key

## Setup

```bash
uv sync
echo "OPENAI_API_KEY=sk-..." > .env
```

## Run

1. Build the vector database (takes about 8 minutes). Re-run it whenever `knowledge-base/` changes:

   ```bash
   uv run ingest.py
   ```

2. Start the chat UI:

   ```bash
   uv run main.py
   ```

   The app opens in your browser at http://127.0.0.1:7860, or the next free port if 7860 is taken. Stop it with `Ctrl+C`.

## Knowledge base

| Folder | Contents |
|---|---|
| `company/` | About, overview, culture, careers |
| `products/` | The 8 Insurellm products |
| `contracts/` | 35 client contracts |
| `employees/` | 35 employee HR records |
