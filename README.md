# Sales101 – RAG-Powered Sales Knowledge Base

A conversational retrieval-augmented generation (RAG) application that ingests
documents from Google Drive and answers questions using Anthropic Claude.

## Stack

- **LLM** – Anthropic Claude (via `langchain-anthropic`)
- **Embeddings** – Voyage AI (`voyage-3`)
- **Vector Store** – ChromaDB (persistent, on-disk)
- **Orchestration** – LangChain
- **Document Sources** – Google Drive (PDFs, Word docs, Google Docs, Sheets, Slides)
- **Chat UI** – Rich-powered CLI

## Quick Start

```bash
# 1. Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys and Google Drive folder IDs

# 4. Set up Google Drive credentials
# Place your OAuth 2.0 credentials.json in the project root.
# See https://developers.google.com/drive/api/quickstart/python

# 5. Ingest documents
python main.py ingest

# 6. Chat
python main.py chat
```

## Project Structure

```
sales101/
├── main.py               # CLI entrypoint (ingest / chat)
├── config.py             # Centralised env-var configuration
├── requirements.txt
├── .env.example
├── ingest/
│   ├── google_drive.py   # Google Drive API client
│   ├── loader.py         # File → LangChain Document loaders
│   └── pipeline.py       # Download → parse → chunk → embed → store
├── rag/
│   ├── embeddings.py     # Voyage AI embeddings
│   ├── vectorstore.py    # ChromaDB vector store
│   └── chain.py          # Conversational retrieval chain (Claude)
└── chat/
    └── cli.py            # Interactive Rich CLI chat
```

## Usage

### Ingest

```bash
# Use folder IDs from .env
python main.py ingest

# Or specify folder IDs directly
python main.py ingest FOLDER_ID_1 FOLDER_ID_2

# Verbose logging
python main.py -v ingest
```

### Chat

```bash
python main.py chat
```

Type your questions at the prompt. The assistant will retrieve relevant chunks
from the vector store and answer using Claude. Type `quit` or `exit` to end.
