import streamlit as st

from src.document_loader import load_documents
from src.vector_store import create_vector_store
from src.rag import get_rag_chain


DOCUMENTS_PATH = "data/documents"


st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 Enterprise Knowledge Assistant")
st.write(
    "Upload enterprise documents and ask questions using AI-powered RAG."
)


# =========================================================
# SESSION STATE
# =========================================================

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# LOAD EXISTING KNOWLEDGE BASE
# =========================================================

if st.session_state.rag_chain is None:

    try:
        st.session_state.rag_chain = get_rag_chain()

    except Exception:
        pass


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📚 Knowledge Base")

    st.write(
        "Place your PDF, DOCX, PPTX or TXT files inside:"
    )

    st.code("data/documents")


    if st.button("🔄 Build Knowledge Base"):

        with st.spinner("Loading documents..."):

            documents = load_documents(DOCUMENTS_PATH)


        if not documents:

            st.error(
                "No documents found. Please add documents to "
                "data/documents first."
            )

        else:

            with st.spinner(
                "Creating FAISS vector database..."
            ):

                create_vector_store(documents)


            st.session_state.rag_chain = get_rag_chain()

            st.success(
                f"Knowledge base created from "
                f"{len(documents)} document sections."
            )


    # Clear chat button
    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# CHAT HISTORY
# =========================================================

st.subheader("💬 Chat")


# Show ALL previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


        # Show sources for assistant messages
        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            st.markdown("### 📄 Sources")

            for source in message["sources"]:

                st.write(f"- {source}")


# =========================================================
# CHAT INPUT
# =========================================================

question = st.chat_input(
    "Ask something about your documents..."
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if question:

    # -----------------------------------------------------
    # SHOW USER QUESTION
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):

        st.markdown(question)


    # -----------------------------------------------------
    # CHECK RAG
    # -----------------------------------------------------

    if st.session_state.rag_chain is None:

        answer = (
            "Please build the Knowledge Base first."
        )

        sources = []


    else:

        # -------------------------------------------------
        # GET ANSWER
        # -------------------------------------------------

        try:

            with st.chat_message("assistant"):

                with st.spinner(
                    "Searching documents..."
                ):

                    answer, sources = (
                        st.session_state.rag_chain(question)
                    )


                st.markdown(answer)


                # Show sources
                if sources:

                    st.markdown("### 📄 Sources")

                    for source in sources:

                        st.write(f"- {source}")


        except Exception as e:

            answer = (
                "⚠️ There was an error while generating "
                "the answer. Please try again."
            )

            sources = []

            with st.chat_message("assistant"):

                st.error(answer)


    # -----------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources
        }
    )