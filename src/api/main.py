from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.rag.retrieve_docs import SupportKnowledgeRetriever
from src.rag.generate_answer import SupportAnswerGenerator


app = FastAPI(
    title="AI Support Copilot API",
    description=(
        "A portfolio API for support ticket assistance using RAG, "
        "semantic retrieval, and support response generation."
    ),
    version="1.0.0"
)


class TicketRequest(BaseModel):
    ticket_text: str = Field(
        ...,
        min_length=5,
        description="Customer support ticket text"
    )
    top_k: Optional[int] = Field(
        3,
        ge=1,
        le=5,
        description="Number of knowledge base chunks to retrieve"
    )


class RetrievedDocument(BaseModel):
    source: str
    chunk_index: int
    distance: float
    content: str


class RetrievalResponse(BaseModel):
    ticket_text: str
    retrieved_documents: List[RetrievedDocument]


class SuggestedReplyResponse(BaseModel):
    ticket_text: str
    suggested_reply: str
    sources_used: List[str]
    generation_method: str
    retrieved_context: List[Dict[str, Any]]


retriever = None
answer_generator = None


@app.on_event("startup")
def startup_event():
    """Load RAG components once when the API starts."""
    global retriever, answer_generator

    retriever = SupportKnowledgeRetriever()
    answer_generator = SupportAnswerGenerator(retriever=retriever)


@app.get("/")
def root():
    return {
        "message": "AI Support Copilot API is running",
        "available_endpoints": [
            "/health",
            "/retrieve",
            "/suggest-reply",
            "/docs"
        ]
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-support-copilot-api"
    }


@app.post("/retrieve", response_model=RetrievalResponse)
def retrieve_documents(request: TicketRequest):
    """Retrieve relevant knowledge base documents for a support ticket."""
    try:
        docs = retriever.retrieve(
            query=request.ticket_text,
            top_k=request.top_k
        )

        return {
            "ticket_text": request.ticket_text,
            "retrieved_documents": docs
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/suggest-reply", response_model=SuggestedReplyResponse)
def suggest_reply(request: TicketRequest):
    """Generate a suggested support reply using retrieved RAG context."""
    try:
        result = answer_generator.generate_answer(
            ticket_text=request.ticket_text,
            top_k=request.top_k
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))