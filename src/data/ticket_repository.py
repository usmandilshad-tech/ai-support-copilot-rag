from typing import Dict, Any, Optional

from sqlalchemy import create_engine, text

from src.utils.config import DATABASE_URL


class TicketRepository:
    """Read support tickets from the MySQL database."""

    def __init__(self):
        self.engine = create_engine(DATABASE_URL)

    def get_ticket_by_id(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single ticket by ticket_id."""
        query = text("""
            SELECT
                ticket_id,
                ticket_type,
                ticket_subject,
                ticket_description,
                ticket_text,
                ticket_status,
                ticket_priority,
                ticket_channel,
                product_purchased,
                customer_satisfaction_rating
            FROM support_tickets
            WHERE ticket_id = :ticket_id
            LIMIT 1
        """)

        with self.engine.connect() as connection:
            result = connection.execute(query, {"ticket_id": ticket_id})
            row = result.mappings().first()

        if row is None:
            return None

        return dict(row)

    def get_recent_tickets(self, limit: int = 10) -> list[Dict[str, Any]]:
        """Fetch recent tickets for testing/demo purposes."""
        query = text("""
            SELECT
                ticket_id,
                ticket_type,
                ticket_subject,
                ticket_status,
                ticket_priority,
                ticket_channel
            FROM support_tickets
            LIMIT :limit
        """)

        with self.engine.connect() as connection:
            result = connection.execute(query, {"limit": limit})
            rows = result.mappings().all()

        return [dict(row) for row in rows]