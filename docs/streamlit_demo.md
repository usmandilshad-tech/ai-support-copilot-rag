# Streamlit Demo App

## Purpose

The Streamlit demo app provides a simple user interface for the AI Support Copilot project.

It allows users to view support tickets from MySQL, select a ticket, generate a RAG-based suggested reply, and inspect the retrieved knowledge base context.

## How to Run

Start MySQL using XAMPP.

Start the FastAPI backend:

```bash
python -B -m uvicorn src.api.main:app --reload