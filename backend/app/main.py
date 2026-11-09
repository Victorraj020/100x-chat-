from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from .config import settings
from .schemas import (
    ChatRequest, ChatResponse, SearchRequest, SearchResponse,
    StoryChapter, KnowledgeSource
)
from .services.vector_store import vector_store
from .services.conversation_memory import conversation_memory
from .services.llm import llm_service
from .services.story_service import story_service
from .services.knowledge_base import KNOWLEDGE_CHUNKS

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize vector store
    print(f"Starting {settings.APP_NAME}...")
    await vector_store.initialize()
    yield
    print("Shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Context-Aware AI Voice Chatbot & Storyteller representing Victorraj",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "llm_provider": llm_service.provider,
        "vector_store_mode": "postgres_pgvector" if vector_store.use_postgres else "in_memory_cosine",
        "knowledge_records_count": len(vector_store.chunks) if not vector_store.use_postgres else "pg_table",
    }

@app.get("/api/story/chapters", response_model=List[StoryChapter])
async def get_story_chapters():
    return story_service.get_all_chapters()

@app.get("/api/story/chapters/{chapter_id}", response_model=StoryChapter)
async def get_story_chapter(chapter_id: str):
    chapter = story_service.get_chapter_by_id(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id or "default-session"
    user_query = request.message.strip()

    if not user_query:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # 1. Retrieve knowledge via Vector Store (RAG)
    retrieved_raw = await vector_store.search(
        query=user_query,
        top_k=settings.TOP_K_RETRIEVAL
    )

    # 2. Get recent conversation context
    history_str = conversation_memory.format_history_for_prompt(session_id)

    # 3. Generate grounded response
    response_text, suggested_followups = await llm_service.generate_response(
        user_message=user_query,
        retrieved_sources=retrieved_raw,
        conversation_history=history_str,
        chapter_context=request.chapter_context
    )

    # 4. Save to conversation memory
    conversation_memory.add_message(session_id, "user", user_query)
    conversation_memory.add_message(session_id, "assistant", response_text)

    # 5. Format sources for auditability and UI inspection
    sources = [
        KnowledgeSource(
            id=s["id"],
            title=s["title"],
            category=s["category"],
            project=s.get("project"),
            similarity_score=s["similarity_score"],
            snippet=s["snippet"]
        )
        for s in retrieved_raw
    ]

    return ChatResponse(
        response=response_text,
        session_id=session_id,
        sources=sources,
        chapter_context=request.chapter_context,
        suggested_followups=suggested_followups
    )

@app.post("/api/chat/clear")
async def clear_chat(session_id: Optional[str] = "default-session"):
    conversation_memory.clear(session_id)
    return {"status": "cleared", "session_id": session_id}

@app.post("/api/knowledge/search", response_model=SearchResponse)
async def search_knowledge(request: SearchRequest):
    results_raw = await vector_store.search(
        query=request.query,
        top_k=request.top_k or 4,
        category=request.category
    )
    sources = [
        KnowledgeSource(
            id=s["id"],
            title=s["title"],
            category=s["category"],
            project=s.get("project"),
            similarity_score=s["similarity_score"],
            snippet=s["snippet"]
        )
        for s in results_raw
    ]
    return SearchResponse(results=sources)

@app.post("/api/knowledge/ingest")
async def reingest_knowledge():
    vector_store.initialized = False
    await vector_store.initialize()
    return {"status": "reindexed", "records": len(vector_store.chunks)}

