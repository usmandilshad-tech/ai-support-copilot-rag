import requests
import pandas as pd
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Support Copilot",
    page_icon="🤖",
    layout="wide"
)


st.title("AI Support Copilot")
st.caption(
    "RAG-powered support assistant using MySQL tickets, Chroma retrieval, "
    "and FastAPI backend."
)


@st.cache_data(ttl=60)
def fetch_recent_tickets(limit: int = 20):
    """Fetch recent tickets from the FastAPI backend."""
    response = requests.get(
        f"{API_BASE_URL}/tickets/recent",
        params={"limit": limit},
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def fetch_ticket(ticket_id: str):
    """Fetch a single ticket by ID."""
    response = requests.get(
        f"{API_BASE_URL}/tickets/{ticket_id}",
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def generate_reply(ticket_id: str, top_k: int = 3):
    """Generate suggested reply for a ticket."""
    response = requests.post(
        f"{API_BASE_URL}/tickets/{ticket_id}/suggest-reply",
        params={"top_k": top_k},
        timeout=60
    )
    response.raise_for_status()
    return response.json()


with st.sidebar:
    st.header("Settings")

    ticket_limit = st.slider(
        "Number of recent tickets",
        min_value=5,
        max_value=50,
        value=20,
        step=5
    )

    top_k = st.slider(
        "Knowledge base chunks to retrieve",
        min_value=1,
        max_value=5,
        value=3,
        step=1
    )

    st.markdown("---")
    st.markdown("### Backend")
    st.code(API_BASE_URL)

    refresh = st.button("Refresh Tickets")


if refresh:
    st.cache_data.clear()


try:
    recent_data = fetch_recent_tickets(limit=ticket_limit)
    tickets = recent_data.get("tickets", [])

except Exception as e:
    st.error(
        "Could not fetch tickets. Make sure FastAPI is running and MySQL is started."
    )
    st.exception(e)
    st.stop()


if not tickets:
    st.warning("No tickets found.")
    st.stop()


ticket_df = pd.DataFrame(tickets)

st.subheader("Recent Support Tickets")
st.dataframe(ticket_df, width="stretch")


ticket_options = [
    f"{ticket['ticket_id']} | {ticket.get('ticket_type')} | {ticket.get('ticket_priority')} | {ticket.get('ticket_subject')}"
    for ticket in tickets
]

selected_option = st.selectbox(
    "Select a ticket",
    ticket_options
)

selected_ticket_id = selected_option.split("|")[0].strip()


try:
    ticket = fetch_ticket(selected_ticket_id)

except Exception as e:
    st.error("Could not fetch selected ticket.")
    st.exception(e)
    st.stop()


st.subheader("Selected Ticket Details")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Ticket ID", ticket.get("ticket_id"))

with col2:
    st.metric("Priority", ticket.get("ticket_priority"))

with col3:
    st.metric("Status", ticket.get("ticket_status"))

with col4:
    st.metric("Channel", ticket.get("ticket_channel"))


detail_col1, detail_col2 = st.columns(2)

with detail_col1:
    st.markdown("### Ticket Metadata")
    st.write("**Type:**", ticket.get("ticket_type"))
    st.write("**Subject:**", ticket.get("ticket_subject"))
    st.write("**Product:**", ticket.get("product_purchased"))
    st.write("**Satisfaction Rating:**", ticket.get("customer_satisfaction_rating"))

with detail_col2:
    st.markdown("### Customer Message")
    st.write(ticket.get("ticket_description"))


st.markdown("---")

if st.button("Generate Suggested Reply", type="primary"):
    with st.spinner("Generating RAG-based support reply..."):
        try:
            result = generate_reply(
                ticket_id=selected_ticket_id,
                top_k=top_k
            )

        except Exception as e:
            st.error("Could not generate reply.")
            st.exception(e)
            st.stop()

    rag_response = result.get("rag_response", {})

    st.subheader("Suggested Support Reply")

    st.text_area(
        "Generated Reply",
        value=rag_response.get("suggested_reply", ""),
        height=250
    )

    st.subheader("Sources Used")

    sources = rag_response.get("sources_used", [])

    if sources:
        for source in sources:
            st.success(source)
    else:
        st.info("No sources returned.")

    st.subheader("Retrieved Knowledge Base Context")

    retrieved_context = rag_response.get("retrieved_context", [])

    for index, context in enumerate(retrieved_context, start=1):
        with st.expander(
            f"Context {index}: {context.get('source')} | Distance: {context.get('distance')}"
        ):
            st.write(context.get("content"))

    with st.expander("Full API Response"):
        st.json(result)