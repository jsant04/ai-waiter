"""
Vector Store Service
---------------------
Handles embedding storage and similarity search using
Supabase + pgvector via LangChain's SupabaseVectorStore.

Supabase table required:  menu_embeddings
RPC function required:    match_menu_items

Both are created by running backend/supabase/migrations.sql
"""

import logging
import os
from typing import List

from langchain.schema import Document
from supabase import Client, create_client

from services.embeddings import get_embeddings

logger = logging.getLogger(__name__)

TABLE_NAME = "menu_embeddings"
QUERY_FUNCTION = "match_menu_items"


# ── Supabase client factory ───────────────────────────────

def get_supabase_client() -> Client:
    """Create and return a Supabase client."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise EnvironmentError(
            "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in the environment."
        )
    return create_client(url, key)


# ── Write: store documents ────────────────────────────────

def store_documents(documents: List[Document], restaurant_id: str) -> int:
    """
    Embed and persist menu documents in Supabase.

    Steps:
      1. Delete all existing embeddings for this restaurant (full refresh).
      2. Insert new embeddings via LangChain SupabaseVectorStore.

    Returns the number of documents stored.
    """
    if not documents:
        return 0

    # Ensure restaurant_id is on every document's metadata
    for doc in documents:
        doc.metadata["restaurant_id"] = restaurant_id

    client = get_supabase_client()

    # ── Step 1: delete old menu for this restaurant ──
    try:
        client.table(TABLE_NAME).delete().eq(
            "restaurant_id", restaurant_id
        ).execute()
        logger.info("Cleared existing embeddings for restaurant '%s'", restaurant_id)
    except Exception as exc:
        logger.warning("Could not clear old embeddings (non-fatal): %s", exc)

    # ── Step 2: embed + insert ────────────────────────
    embeddings = get_embeddings()
    SupabaseVectorStore.from_documents(
        documents,
        embeddings,
        client=client,
        table_name=TABLE_NAME,
        query_name=QUERY_FUNCTION,
        chunk_size=50,  # batch size for embedding API calls
    )

    logger.info(
        "Stored %d menu embeddings for restaurant '%s'",
        len(documents),
        restaurant_id,
    )
    return len(documents)


# ── Read: similarity search ───────────────────────────────

def search_menu(query: str, restaurant_id: str, k: int = 5) -> List[Document]:
    """
    Retrieve the top-k most relevant menu items for a user query.

    Calls the match_menu_items RPC directly to avoid LangChain/supabase
    client version incompatibilities with SupabaseVectorStore.similarity_search.
    """
    try:
        client = get_supabase_client()
        embeddings = get_embeddings()

        # Embed the query
        query_vector = embeddings.embed_query(query)

        # Call the RPC directly with a metadata filter for restaurant_id
        response = client.rpc(
            QUERY_FUNCTION,
            {
                "query_embedding": query_vector,
                "match_count": k,
                "filter": {"restaurant_id": restaurant_id},
            },
        ).execute()

        docs = [
            Document(
                page_content=row["content"],
                metadata=row.get("metadata", {}),
            )
            for row in (response.data or [])
        ]

        logger.info(
            "Found %d relevant documents for query='%s' restaurant='%s'",
            len(docs),
            query,
            restaurant_id,
        )
        return docs

    except Exception as exc:
        logger.error("Vector search failed: %s", exc, exc_info=True)
        return []
