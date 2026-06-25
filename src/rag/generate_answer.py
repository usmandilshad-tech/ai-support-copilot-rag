from typing import List, Dict, Any

from src.rag.retrieve_docs import SupportKnowledgeRetriever


class SupportAnswerGenerator:
    """
    Generate a support response using retrieved knowledge base context.

    This first version uses a structured template instead of an external LLM.
    Later, this can be upgraded to use OpenAI, Azure OpenAI, or another LLM.
    """

    def __init__(self, retriever: SupportKnowledgeRetriever | None = None):
        self.retriever = retriever or SupportKnowledgeRetriever()

    def generate_answer(self, ticket_text: str, top_k: int = 3) -> Dict[str, Any]:
        """Generate a support reply based on retrieved knowledge base documents."""
        if not ticket_text or not ticket_text.strip():
            raise ValueError("ticket_text cannot be empty.")

        retrieved_docs = self.retriever.retrieve(ticket_text, top_k=top_k)

        sources = []
        context_points = []

        for doc in retrieved_docs:
            source = doc["source"]

            if source not in sources:
                sources.append(source)

            context_points.append({
                "source": source,
                "distance": doc["distance"],
                "content": doc["content"]
            })

        reply = self._build_template_reply(ticket_text, context_points)

        return {
            "ticket_text": ticket_text,
            "suggested_reply": reply,
            "sources_used": sources,
            "retrieved_context": context_points,
            "generation_method": "template_based_rag_v1"
        }

    def _build_template_reply(
        self,
        ticket_text: str,
        context_points: List[Dict[str, Any]]
    ) -> str:
        """Build a structured support reply from retrieved context."""

        combined_context = "\n\n".join(
            point["content"] for point in context_points
        ).lower()

        if "charged twice" in ticket_text.lower() or "duplicate" in ticket_text.lower():
            reply = (
                "Thank you for contacting us. I understand that you may have been charged more than once, "
                "and I’m sorry for the concern this has caused.\n\n"
                "To help us review this properly, please share your order number or transaction reference, "
                "the payment date, and the charged amount. We will check whether one transaction is still pending "
                "or whether both charges were completed.\n\n"
                "If both charges were completed, we will forward the case to our billing team for refund review. "
                "Billing verification may take 3 to 5 business days."
            )

        elif "cancel" in ticket_text.lower() or "cancellation" in ticket_text.lower():
            reply = (
                "Thank you for reaching out. I can help guide you with the cancellation request.\n\n"
                "Please share the account email and subscription ID or order number so we can confirm the active "
                "subscription or order status. Once verified, we can confirm whether the cancellation takes effect "
                "immediately or at the end of the current billing cycle.\n\n"
                "We will not mark the cancellation as completed until it has been fully processed."
            )

        elif "login" in ticket_text.lower() or "password" in ticket_text.lower() or "account" in ticket_text.lower():
            reply = (
                "Thank you for contacting support. I’m sorry you are having trouble accessing your account.\n\n"
                "Please confirm the email address linked to your account and let us know whether you recently changed "
                "your password. You can also try clearing your browser cache and cookies, or testing from another "
                "browser or device.\n\n"
                "If the password reset still does not work, we will escalate this to the technical support team for review."
            )

        elif "device" in ticket_text.lower() or "compatible" in ticket_text.lower() or "compatibility" in ticket_text.lower():
            reply = (
                "Thank you for your question. I can help check product compatibility for you.\n\n"
                "Please share the exact product name or model, along with the device, software, or platform you want "
                "to use it with. Once we have those details, we can confirm compatibility or forward the question to "
                "technical support if further review is needed."
            )

        elif "angry" in ticket_text.lower() or "escalate" in ticket_text.lower() or "manager" in ticket_text.lower():
            reply = (
                "Thank you for sharing this. I understand that the customer is dissatisfied and that the issue may need "
                "additional attention.\n\n"
                "Please include the customer name or account ID, ticket ID, issue summary, steps already taken, and any "
                "screenshots, logs, or supporting details. Based on the situation, this can be escalated to customer "
                "success, management, billing, or technical support.\n\n"
                "The escalation note should clearly state the requested action and priority level."
            )
        elif (
            "hardware" in ticket_text.lower()
            or "strange noises" in ticket_text.lower()
            or "not functioning" in ticket_text.lower()
            or "not working" in ticket_text.lower()
            or "intermittent" in ticket_text.lower()
            ):
            reply = (
                "Thank you for contacting support. I’m sorry to hear that your product is making unusual noises "
                "and is not functioning properly.\n\n"
                "To help us investigate this further, please confirm the exact product model, when the issue first started, "
                "whether the noise happens continuously or only at certain times, and whether any error message or warning "
                "indicator appears. Please also let us know if you have already tried restarting or resetting the product.\n\n"
                "Because this may involve a hardware-related issue, we may need to escalate the case to our technical support "
                "team after reviewing these details. Screenshots, short videos, or any additional evidence of the issue would "
                "also help us diagnose the problem more quickly."
                )
        else:
            reply = (
                "Thank you for contacting support. I’m sorry for the inconvenience you are experiencing.\n\n"
                "To help us review this properly, please share the relevant account details, order number, product name, "
                "and any screenshots or error messages if available. We will review the information and guide you on "
                "the next steps.\n\n"
                "If the issue cannot be resolved at first level, we will escalate it to the appropriate team."
            )

        return reply


def main() -> None:
    print("Starting support answer generation test...", flush=True)

    generator = SupportAnswerGenerator()

    sample_tickets = [
        "I was charged twice for my order and need help with the payment.",
        "I want to cancel my subscription.",
        "I cannot login to my account after resetting my password.",
        "I want to know if the product works with my device.",
        "The customer is angry and wants to escalate the issue."
    ]

    for ticket in sample_tickets:
        print("\n" + "=" * 100, flush=True)
        print("Ticket:", ticket, flush=True)
        print("=" * 100, flush=True)

        result = generator.generate_answer(ticket_text=ticket, top_k=2)

        print("\nSuggested Reply:\n", flush=True)
        print(result["suggested_reply"], flush=True)

        print("\nSources Used:", result["sources_used"], flush=True)
        print("-" * 100, flush=True)

    print("Support answer generation test completed.", flush=True)


if __name__ == "__main__":
    main()