
import streamlit as st

from config import *



from auth.gmail_auth import get_gmail_service
from gmail.fetch_emails import fetch_emails_from_account
from gmail.send_email import send_email

from config.accounts import GMAIL_ACCOUNTS
from config.settings import GMAIL_QUERY, MAX_EMAILS_PER_ACCOUNT

from rag.chunker import chunk_emails
from rag.vector_store import SimpleVectorStore
from rag.rag_pipeline import generate_rag_answer

from llm.email_generator import generate_email_reply

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Gmail RAG Assistant",
    page_icon="",
    layout="wide"
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
            
/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main {
    background-color: #F7F8FA;
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* ── Page title ── */
.page-title {
    font-size: 28px;
    font-weight: 600;
    color: #111827;
    letter-spacing: -0.5px;
    margin-bottom: 2px;
}

.page-subtitle {
    font-size: 15px;
    color: #6B7280;
    margin-bottom: 32px;
    font-weight: 400;
}

/* ── Section headings ── */
h2, h3, .stSubheader {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    color: #111827 !important;
    letter-spacing: -0.3px !important;
}

/* ── Dividers ── */
hr {
    border: none;
    border-top: 1px solid #E5E7EB;
    margin: 20px 0;
}

/* ── Input fields ── */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    box-shadow: none !important;
    transition: border-color 0.2s ease;
}

.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important;
}

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    border-radius: 8px;
    height: 2.75em;
    font-weight: 500;
    font-size: 14px;
    font-family: 'DM Sans', sans-serif;
    border: none;
    background: #1D4ED8;
    color: #FFFFFF;
    letter-spacing: 0.2px;
    transition: background 0.18s ease, box-shadow 0.18s ease;
}

.stButton > button:hover {
    background: #1E40AF;
    box-shadow: 0 2px 8px rgba(29,78,216,0.25);
    color: #FFFFFF;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid #E5E7EB;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    font-weight: 500;
    color: #6B7280;
    padding: 10px 20px;
    border-radius: 6px 6px 0 0;
    border: none;
    background: transparent;
}

.stTabs [aria-selected="true"] {
    color: #1D4ED8 !important;
    border-bottom: 2px solid #1D4ED8 !important;
    background: transparent !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

section[data-testid="stSidebar"] * {
    font-family: 'DM Sans', sans-serif;
    color: #374151;
}

section[data-testid="stSidebar"] .stSuccess {
    background-color: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 6px;
    color: #166534 !important;
    font-size: 13px;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
    color: #374151 !important;
    background-color: #F9FAFB !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 6px !important;
}

.streamlit-expanderContent {
    background-color: #F9FAFB !important;
    border: 1px solid #E5E7EB !important;
    border-top: none !important;
    border-radius: 0 0 6px 6px !important;
}

/* ── Code blocks ── */
.stCode, code {
    font-family: 'DM Mono', monospace !important;
    font-size: 12.5px !important;
    background-color: #F3F4F6 !important;
    border-radius: 6px !important;
    color: #1F2937 !important;
}

/* ── Slider ── */
.stSlider > div > div > div {
    color: #1D4ED8 !important;
}
/* ── Fix sidebar collapse button icon ── */
button[data-testid="collapsedControl"] {
    font-family: 'Material Icons' !important;
}

/* ── Success / Warning / Error banners ── */
.stSuccess {
    border-radius: 8px;
    font-size: 14px;
}

.stWarning {
    border-radius: 8px;
    font-size: 14px;
}

.stError {
    border-radius: 8px;
    font-size: 14px;
}

/* ── Caption / footer ── */
.stCaption {
    color: #9CA3AF !important;
    font-size: 12px !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-color: #1D4ED8 transparent transparent transparent !important;
}

/* ── Section label utility ── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #9CA3AF;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<div class="page-title">Gmail Assistant</div>
<div class="page-subtitle">Search, understand, and compose emails with AI</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# INITIALIZE SYSTEM
# ═══════════════════════════════════════════════════════════════

if 'vector_store' not in st.session_state:

    with st.spinner("Connecting Gmail accounts..."):

        services = {}

        for account in GMAIL_ACCOUNTS:

            services[account] = get_gmail_service(account)

    all_emails = []

    with st.spinner("Fetching emails..."):

        for account, service in services.items():

            emails = fetch_emails_from_account(
                service,
                account,
                GMAIL_QUERY,
                MAX_EMAILS_PER_ACCOUNT
            )

            all_emails.extend(emails)

    with st.spinner("Processing email chunks..."):

        chunks = chunk_emails(all_emails)

    with st.spinner("Building vector index..."):

        vector_store = SimpleVectorStore()

        vector_store.add_documents(chunks)

    st.session_state.vector_store = vector_store
    st.session_state.services = services

    st.success("System ready")

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:

    st.markdown("### System Info")

    st.markdown(f"""
    <div class="section-label">Configuration</div>

    **Connected Accounts**  
    {len(GMAIL_ACCOUNTS)}

    **Emails Indexed**  
    {MAX_EMAILS_PER_ACCOUNT * len(GMAIL_ACCOUNTS)}

    **LLM**  
    llama-3.3-70b-versatile

    **Embeddings**  
    sentence-transformers
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="section-label">Gmail Accounts</div>', unsafe_allow_html=True)

    for acc in GMAIL_ACCOUNTS:
        st.success(acc)

# ═══════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════

tab1, tab2 = st.tabs([
    "Ask Questions",
    "Compose & Send"
])

# ═══════════════════════════════════════════════════════════════
# TAB 1 — RAG SEARCH
# ═══════════════════════════════════════════════════════════════

with tab1:

    st.subheader("Ask Questions About Your Emails")

    query = st.text_input(
        "Your question",
        placeholder="Who sent me payment-related emails?"
    )

    top_k = st.slider(
        "Number of context chunks to retrieve",
        1,
        10,
        5
    )

    ask_button = st.button("Search Emails")

    if ask_button:

        if query.strip() == "":
            st.warning("Please enter a question.")
        else:

            with st.spinner("Searching and generating answer..."):

                docs = st.session_state.vector_store.search(
                    query,
                    k=top_k
                )

                answer = generate_rag_answer(
                    query,
                    docs
                )

            st.divider()

            st.subheader("Answer")
            st.write(answer)

            st.divider()

            st.subheader("Retrieved Context")

            for i, doc in enumerate(docs):

                with st.expander(
                    f"Context {i+1}  —  Score: {doc['score']:.3f}"
                ):

                    st.code(doc['text'])

# ═══════════════════════════════════════════════════════════════
# TAB 2 — SEND EMAIL
# ═══════════════════════════════════════════════════════════════

with tab2:

    col1, col2 = st.columns([1, 1])

    # ═══════════════════════════════════════════════
    # LEFT SIDE
    # ═══════════════════════════════════════════════

    with col1:

        st.subheader("Compose Email")

        selected_account = st.selectbox(
            "Send From",
            GMAIL_ACCOUNTS
        )

        recipient = st.text_input(
            "Recipient",
            placeholder="example@gmail.com"
        )

        subject = st.text_input(
            "Subject",
            placeholder="Meeting Follow-up"
        )

        instruction = st.text_area(
            "Instructions for AI",
            height=220,
            placeholder="Example: Write a professional email asking for an internship update. Mention that I am excited about the opportunity. Keep it concise."
        )

        tone = st.selectbox(
            "Tone",
            [
                "Professional",
                "Friendly",
                "Formal",
                "Concise"
            ]
        )

        generate_btn = st.button("Generate Email")

    # ═══════════════════════════════════════════════
    # RIGHT SIDE
    # ═══════════════════════════════════════════════

    with col2:

        st.subheader("Generated Email")

        if 'generated_email' not in st.session_state:
            st.session_state.generated_email = ""

        if generate_btn:

            if instruction.strip() == "":
                st.warning("Please enter instructions.")
            else:

                with st.spinner("Generating email..."):

                    generated_email = generate_email_reply(
                        "",
                        f"""
Subject: {subject}

Instruction:
{instruction}

Tone:
{tone}
"""
                    )

                    st.session_state.generated_email = generated_email

        email_body = st.text_area(
            "Review and edit before sending",
            value=st.session_state.generated_email,
            height=350
        )

        send_btn = st.button("Send Email")

        # ═══════════════════════════════════════════
        # SEND EMAIL
        # ═══════════════════════════════════════════

        if send_btn:

            if (
                recipient.strip() == ""
                or subject.strip() == ""
                or email_body.strip() == ""
            ):

                st.error("Please complete all fields before sending.")

            else:

                try:

                    service = st.session_state.services[
                        selected_account
                    ]

                    send_email(
                        service=service,
                        sender=selected_account,
                        to=recipient,
                        subject=subject,
                        body_text=email_body
                    )

                    st.success("Email sent successfully.")

                except Exception as e:

                    st.error(f"Failed to send email: {e}")

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════

st.divider()

st.caption(
    "Built to assist with email management and composition using AI. Always review generated content before sending."
)