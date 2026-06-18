# API Usage

## Purpose

The AI Support Copilot API exposes the RAG retrieval and support reply generation pipeline through a FastAPI backend.

## Run the API

```bash
python -B -m uvicorn src.api.main:app --reload

API Base URL
http://127.0.0.1:8000

API Interactive Documentation

http://127.0.0.1:8000/docs

Health Check
GET /health

Retrieve Knowledge Base Context
POST /retrieve

Example request:

{
  "ticket_text": "I was charged twice for my order and need help with the payment.",
  "top_k": 2
}
Generate Suggested Reply
POST /suggest-reply

Example request:

{
  "ticket_text": "I cannot login to my account after resetting my password.",
  "top_k": 2
}