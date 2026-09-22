from dotenv import load_dotenv
from langchain_community.embeddings import FastEmbedEmbeddings

load_dotenv()


def get_embeddings():
    """
    Create and return local FastEmbed embedding model.
    """

    embeddings = FastEmbedEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    return embeddings

