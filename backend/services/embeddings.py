"""
Embeddings Service
------------------
Provides a shared OpenAI Embeddings instance used throughout the app.
"""
import os
from langchain_openai import OpenAIEmbeddings


def get_embeddings() -> OpenAIEmbeddings:
    """Return a configured OpenAI Embeddings instance."""
    return OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
