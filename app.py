import streamlit as st
import tempfile
from main.logger_config import setup_logger
from main.pdf_processor import PDFProcessor
from main.vector_store import VectorStoreBuilder
from main.query_engine import QueryEngine


setup_logger()

# Streamlit UI Setup
st.set_page_config(page_title="RAG PDF Chat", layout="wide")


# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vector_db" not in st.session_state:
    st.session_state.vector_db = None
if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False


def cleanup_vector_db():
    if st.session_state.get("vector_db", False):
        st.session_state.vector_db.delete_collection()


# Clear Function
def clear_session_state_and_vector_db():
    """Clear the session state and vector database."""

    st.session_state.clear()
    st.success("✅ Vector DB & session state cleared.")


# Header with Clear DB button on right
col1, col_spacer, col2 = st.columns([6, 1, 1])
with col1:
    st.markdown(
        "<h1 style='text-align: left;'>📄 RAG Chat with Your PDF</h1>",
        unsafe_allow_html=True,
    )
with col2:
    st.button("🗑️ Clear DB", key="clear_db", on_click=clear_session_state_and_vector_db)


# Columns
left_col, right_col = st.columns([1, 2])

import hashlib


def get_file_hash(file_data):
    return hashlib.md5(file_data).hexdigest()


# LEFT: Upload
with left_col:
    st.markdown("### 📤 Upload Your PDF")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf", key="uploaded_file")

    if uploaded_file:
        file_bytes = uploaded_file.read()
        file_hash = get_file_hash(file_bytes)

        if st.session_state.get("last_file_hash") != file_hash:
            st.session_state.last_file_hash = file_hash
            st.session_state.pdf_uploaded = True

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(file_bytes)
                pdf_path = tmp_file.name

            st.success("✅ PDF uploaded successfully.")
            with st.spinner("🔍 Creating vector DB..."):
                chunks = PDFProcessor().load_and_split(pdf_path)
                st.session_state.vector_db = VectorStoreBuilder().create_vector_db(
                    chunks
                )
            st.success("✅ Embeddings created.")

# RIGHT: Chat
with right_col:
    st.markdown("### 💬 Ask Questions")
    if st.session_state.vector_db:
        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([5, 1])
            with col1:
                user_query = st.text_input(
                    "Your question:",
                    label_visibility="collapsed",
                    placeholder="Type here...",
                )
            with col2:
                submitted = st.form_submit_button("📤")

        if submitted and user_query.strip():
            with st.spinner("🤖 Generating answer..."):
                answer = QueryEngine().get_answer(
                    st.session_state.vector_db, user_query
                )
                st.session_state.chat_history.append((user_query, answer))

        for q, a in st.session_state.chat_history:
            st.markdown(f"<b>🟢 You:</b> {q}", unsafe_allow_html=True)
            st.markdown(f"<b>🤖 Answer:</b> {a}", unsafe_allow_html=True)
    else:
        st.info("📎 Please upload a PDF to start chatting.")
