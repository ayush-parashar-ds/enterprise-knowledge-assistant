from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .embeddings import get_embeddings


VECTORSTORE_PATH = Path("vectorstore")


def create_vector_store(documents):
    """
    Split documents into chunks and create FAISS vector store.
    """

    if not documents:
        raise ValueError("No documents found to create vector store.")

    # Split documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = text_splitter.split_documents(documents)

    # Create local embeddings
    embeddings = get_embeddings()

    # Create FAISS vector database
    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    # Save vector database
    vector_store.save_local(str(VECTORSTORE_PATH))

    return vector_store


def load_vector_store():
    """
    Load existing FAISS vector store.
    """

    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        str(VECTORSTORE_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vector_store