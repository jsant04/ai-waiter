-- ============================================================
--  AI Waiter – Supabase Database Setup
--  Run this in Supabase > SQL Editor (once per project)
-- ============================================================

-- 1. Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- 2. Menu Embeddings Table
--    Stores one row per menu item (embedding + metadata).
-- ============================================================
CREATE TABLE IF NOT EXISTS menu_embeddings (
  id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  content       TEXT        NOT NULL,
  metadata      JSONB       NOT NULL DEFAULT '{}'::JSONB,
  embedding     VECTOR(1536),
  restaurant_id TEXT        NOT NULL DEFAULT 'default',
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index: cosine similarity search (ivfflat for approximate NN)
CREATE INDEX IF NOT EXISTS menu_embeddings_embedding_idx
  ON menu_embeddings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Index: fast tenant filtering
CREATE INDEX IF NOT EXISTS menu_embeddings_restaurant_id_idx
  ON menu_embeddings (restaurant_id);

-- ============================================================
-- 3. match_menu_items RPC
--    Called by LangChain's SupabaseVectorStore for similarity search.
--    The 'filter' parameter maps to metadata @> filter (JSONB containment),
--    which is how LangChain passes restaurant_id as a metadata filter.
-- ============================================================
CREATE OR REPLACE FUNCTION match_menu_items(
  query_embedding VECTOR(1536),
  match_count     INT     DEFAULT 5,
  filter          JSONB   DEFAULT '{}'::JSONB
)
RETURNS TABLE (
  id         UUID,
  content    TEXT,
  metadata   JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    me.id,
    me.content,
    me.metadata,
    1 - (me.embedding <=> query_embedding) AS similarity
  FROM menu_embeddings me
  WHERE
    me.embedding IS NOT NULL
    AND (filter = '{}'::JSONB OR me.metadata @> filter)
  ORDER BY me.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- ============================================================
-- 4. Conversations Table  (optional — for analytics)
--    Logs every user turn and AI reply for dashboard features.
-- ============================================================
CREATE TABLE IF NOT EXISTS conversations (
  id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id    TEXT        NOT NULL,
  restaurant_id TEXT        NOT NULL DEFAULT 'default',
  role          TEXT        NOT NULL CHECK (role IN ('user', 'assistant')),
  content       TEXT        NOT NULL,
  is_on_topic   BOOLEAN     DEFAULT TRUE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS conversations_session_id_idx
  ON conversations (session_id);

CREATE INDEX IF NOT EXISTS conversations_restaurant_id_idx
  ON conversations (restaurant_id);

CREATE INDEX IF NOT EXISTS conversations_created_at_idx
  ON conversations (created_at DESC);

-- ============================================================
-- 5. Row-Level Security (recommended for production)
-- ============================================================
-- Enable RLS on both tables (service-role key bypasses RLS by default)
ALTER TABLE menu_embeddings  ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations     ENABLE ROW LEVEL SECURITY;

-- Allow service-role full access (used by the FastAPI backend)
CREATE POLICY "service_role_all_menu"
  ON menu_embeddings FOR ALL
  USING (TRUE)
  WITH CHECK (TRUE);

CREATE POLICY "service_role_all_conversations"
  ON conversations FOR ALL
  USING (TRUE)
  WITH CHECK (TRUE);

-- ============================================================
-- Done! Your database is ready for the AI Waiter backend.
-- ============================================================
