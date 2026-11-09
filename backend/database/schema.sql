-- PostgreSQL + pgvector Schema for AI Chatbot (Victorraj Profile)

-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Knowledge documents table
CREATE TABLE IF NOT EXISTS knowledge_documents (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    project TEXT,
    content TEXT NOT NULL,
    tags TEXT[],
    embedding vector(768),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create HNSW index for fast vector cosine similarity search
CREATE INDEX IF NOT EXISTS knowledge_documents_embedding_hnsw_idx 
ON knowledge_documents 
USING hnsw (embedding vector_cosine_ops);

-- Conversation sessions table
CREATE TABLE IF NOT EXISTS chat_sessions (
    id TEXT PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Conversation messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id TEXT REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    sources JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Fast retrieval query helper function
CREATE OR REPLACE FUNCTION match_knowledge_documents (
    query_embedding vector(768),
    match_threshold float,
    match_count int,
    filter_category text DEFAULT NULL,
    filter_project text DEFAULT NULL
)
RETURNS TABLE (
    id text,
    title text,
    category text,
    project text,
    content text,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        kd.id,
        kd.title,
        kd.category,
        kd.project,
        kd.content,
        1 - (kd.embedding <=> query_embedding) AS similarity
    FROM knowledge_documents kd
    WHERE (1 - (kd.embedding <=> query_embedding)) > match_threshold
      AND (filter_category IS NULL OR kd.category = filter_category)
      AND (filter_project IS NULL OR kd.project = filter_project)
    ORDER BY kd.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
