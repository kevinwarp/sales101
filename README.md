# Sales101 — RAG over Google Drive Documents

A conversational Retrieval-Augmented Generation (RAG) application that ingests documents from Google Drive and answers questions about them using Claude.

## Stack

- **LLM** – Anthropic Claude (via `langchain-anthropic`)
- **Embeddings** – Voyage AI (via `langchain-voyageai`)
- **Vector Store** – ChromaDB (persistent, local)
- **Framework** – LangChain
- **Document Sources** – Google Drive (PDFs, Word docs, Google Docs, Sheets, Slides)

## Project Structure

```
sales101/
├── main.py                  # CLI entry point (ingest / chat)
├── config/
│   └── settings.py          # Centralised env-based configuration
├── ingestion/
│   ├── google_drive.py      # Google Drive API client
│   ├── parsers.py           # File-type loaders (PDF, DOCX, XLSX, PPTX, CSV)
│   └── pipeline.py          # Download → parse → chunk → store pipeline
├── vectorstore/
│   └── store.py             # ChromaDB + Voyage AI embeddings
├── rag/
│   ├── chain.py             # History-aware retrieval chain with Claude
│   └── prompts.py           # Prompt templates
├── chat/
│   └── interface.py         # Interactive terminal chat
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

### 1. Install dependencies

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your API keys and Google Drive folder ID.
```

### 3. Google Drive credentials

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Drive API**.
3. Create **OAuth 2.0 Client ID** credentials (Desktop app).
4. Download the JSON and save it as `credentials.json` in the project root.

On the first run the app will open a browser for OAuth consent and save `token.json` locally.

## Usage

### Ingest documents

```bash
python main.py ingest                         # uses GOOGLE_DRIVE_FOLDER_ID from .env
python main.py ingest --folder-id <FOLDER_ID> # override folder
```

### Chat

```bash
python main.py chat
```

Type questions and receive answers grounded in your ingested documents. Chat history is maintained for follow-up questions.
