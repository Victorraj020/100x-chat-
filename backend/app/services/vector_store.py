import json
import os
import numpy as np
from typing import List, Dict, Any, Optional
from ..config import settings
from .knowledge_base import KNOWLEDGE_CHUNKS
from .embeddings import embedding_service

class VectorStore:
    def __init__(self):
        self.use_postgres = False
        self.chunks: List[Dict[str, Any]] = []
        self.embeddings_matrix: Optional[np.ndarray] = None
        self.initialized = False
        
        # Check if database url is provided
        if settings.DATABASE_URL and ("postgresql://" in settings.DATABASE_URL or "postgres://" in settings.DATABASE_URL):
            try:
                import asyncpg
                self.use_postgres = True
            except ImportError:
                print("[VectorStore] asyncpg not installed, falling back to in-memory store.")
                self.use_postgres = False

    async def initialize(self):
        """Index and load the personal knowledge chunks into the vector store."""
        if self.initialized:
            return

        print("[VectorStore] Initializing vector store...")
        if self.use_postgres:
            try:
                await self._init_postgres()
                print("[VectorStore] Connected to PostgreSQL + pgvector successfully.")
                self.initialized = True
                return
            except Exception as e:
                print(f"[VectorStore] Failed to connect to PostgreSQL: {e}. Falling back to in-memory store.")
                self.use_postgres = False

        await self._init_in_memory()
        self.initialized = True
        print(f"[VectorStore] In-memory store ready with {len(self.chunks)} knowledge records.")

    async def _init_postgres(self):
        import asyncpg
        conn = await asyncpg.connect(settings.DATABASE_URL)
        try:
            # Create extension if permitted
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            # Create documents table
            await conn.execute(f"""
                CREATE TABLE IF NOT EXISTS knowledge_documents (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    project TEXT,
                    content TEXT NOT NULL,
                    tags TEXT[],
                    embedding vector({settings.VECTOR_DIMENSION}),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)

            # Ingest initial chunks if empty
            count = await conn.fetchval("SELECT COUNT(*) FROM knowledge_documents;")
            if count == 0:
                print("[VectorStore] Ingesting initial knowledge chunks into PostgreSQL...")
                for item in KNOWLEDGE_CHUNKS:
                    vec = await embedding_service.get_embedding(item["content"])
                    await conn.execute("""
                        INSERT INTO knowledge_documents (id, title, category, project, content, tags, embedding)
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                        ON CONFLICT (id) DO UPDATE SET
                            title = EXCLUDED.title,
                            category = EXCLUDED.category,
                            project = EXCLUDED.project,
                            content = EXCLUDED.content,
                            tags = EXCLUDED.tags,
                            embedding = EXCLUDED.embedding;
                    """, item["id"], item["title"], item["category"], item.get("project"), item["content"], item.get("tags", []), str(vec))
        finally:
            await conn.close()

    async def _init_in_memory(self):
        """Index all knowledge chunks in memory and compute their embeddings."""
        self.chunks = list(KNOWLEDGE_CHUNKS)
        vectors = []
        for item in self.chunks:
            # Combine title, category, tags, and content for a richer embedding representation
            rich_text = f"{item['title']} - Category: {item['category']} (Project: {item.get('project', 'General')}) {item['content']}"
            vec = await embedding_service.get_embedding(rich_text)
            item["embedding"] = vec
            vectors.append(vec)

        self.embeddings_matrix = np.array(vectors, dtype=np.float32)

    async def search(
        self,
        query: str,
        top_k: int = 4,
        category: Optional[str] = None,
        project: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Semantic search with cosine similarity and metadata filtering."""
        if not self.initialized:
            await self.initialize()

        query_vec = await embedding_service.get_embedding(query)
        
        if self.use_postgres:
            return await self._search_postgres(query_vec, top_k, category, project)
        else:
            return await self._search_in_memory(query_vec, top_k, category, project)

    async def _search_postgres(self, query_vec: List[float], top_k: int, category: Optional[str], project: Optional[str]):
        import asyncpg
        conn = await asyncpg.connect(settings.DATABASE_URL)
        try:
            query = """
                SELECT id, title, category, project, content,
                       1 - (embedding <=> $1::vector) as similarity
                FROM knowledge_documents
                WHERE ($2::text IS NULL OR category = $2)
                  AND ($3::text IS NULL OR project = $3)
                ORDER BY embedding <=> $1::vector ASC
                LIMIT $4;
            """
            rows = await conn.fetch(query, str(query_vec), category, project, top_k)
            results = []
            for r in rows:
                results.append({
                    "id": r["id"],
                    "title": r["title"],
                    "category": r["category"],
                    "project": r["project"],
                    "content": r["content"],
                    "similarity_score": round(float(r["similarity"]), 4),
                    "snippet": r["content"][:200] + "..." if len(r["content"]) > 200 else r["content"]
                })
            return results
        finally:
            await conn.close()

    async def _search_in_memory(self, query_vec: List[float], top_k: int, category: Optional[str], project: Optional[str]):
        if self.embeddings_matrix is None or len(self.chunks) == 0:
            return []

        q_arr = np.array(query_vec, dtype=np.float32)
        q_norm = np.linalg.norm(q_arr)
        if q_norm > 0:
            q_arr = q_arr / q_norm

        matrix_norms = np.linalg.norm(self.embeddings_matrix, axis=1, keepdims=True)
        # Avoid division by zero
        matrix_norms[matrix_norms == 0] = 1.0
        normalized_matrix = self.embeddings_matrix / matrix_norms

        similarities = np.dot(normalized_matrix, q_arr)

        scored_chunks = []
        for idx, score in enumerate(similarities):
            chunk = self.chunks[idx]
            
            # Apply metadata filtering if specified
            if category and chunk.get("category") != category:
                continue
            if project and chunk.get("project") != project:
                continue

            scored_chunks.append({
                "id": chunk["id"],
                "title": chunk["title"],
                "category": chunk["category"],
                "project": chunk.get("project"),
                "content": chunk["content"],
                "similarity_score": round(float(score), 4),
                "snippet": chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"]
            })

        # Sort descending by similarity
        scored_chunks.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored_chunks[:top_k]

vector_store = VectorStore()
