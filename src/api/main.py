from contextlib import asynccontextmanager
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.rag.retrieve_docs import SupportKnowledgeRetriever
from src.rag.generate_answer import SupportAnswerGenerator
from src.data.ticket_repository import TicketRepository






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
ticket_repository = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load API components once when the API starts."""
    global retriever, answer_generator, ticket_repository

    retriever = SupportKnowledgeRetriever()
    answer_generator = SupportAnswerGenerator(retriever=retriever)
    ticket_repository = TicketRepository()

    yield

    retriever = None
    answer_generator = None
    ticket_repository = None


app = FastAPI(
    title="AI Support Copilot API",
    description=(
        "A portfolio API for support ticket assistance using RAG, "
        "semantic retrieval, and support response generation."
    ),
    version="1.0.0",
    lifespan=lifespan
)

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
    
@app.get("/tickets/recent")
def get_recent_tickets(limit: int = 10):
    """Return recent support tickets from MySQL."""
    try:
        tickets = ticket_repository.get_recent_tickets(limit=limit)
        return {
            "count": len(tickets),
            "tickets": tickets
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    """Return a support ticket from MySQL by ticket ID."""
    try:
        ticket = ticket_repository.get_ticket_by_id(ticket_id)

        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found")

        return ticket

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tickets/{ticket_id}/suggest-reply")
def suggest_reply_for_ticket(ticket_id: str, top_k: int = 3):
    """Fetch a ticket from MySQL and generate a suggested RAG reply."""
    try:
        ticket = ticket_repository.get_ticket_by_id(ticket_id)

        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found")

        ticket_text = ticket.get("ticket_text")

        if not ticket_text:
            ticket_text = f"{ticket.get('ticket_subject', '')} {ticket.get('ticket_description', '')}"

        product_name = str(ticket.get("product_purchased") or "the product")

        ticket_text = ticket_text.replace("{product_purchased}", product_name)
        ticket_text = ticket_text.replace("}", "")

        enhanced_ticket_text = f"""
Ticket Type: {ticket.get("ticket_type")}
Priority: {ticket.get("ticket_priority")}
Status: {ticket.get("ticket_status")}
Channel: {ticket.get("ticket_channel")}
Product: {ticket.get("product_purchased")}

Customer Message:
{ticket_text}
"""

        result = answer_generator.generate_answer(
            ticket_text=enhanced_ticket_text,
            top_k=top_k
        )

        return {
            "ticket": ticket,
            "rag_response": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))