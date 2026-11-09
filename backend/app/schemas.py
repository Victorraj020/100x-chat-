from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    role: str = Field(..., description="'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message text content")
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str = Field(..., description="User question or statement")
    session_id: Optional[str] = Field("default-session", description="Conversation session ID")
    chapter_context: Optional[str] = Field(None, description="Current story chapter context if any")

class KnowledgeSource(BaseModel):
    id: str
    title: str
    category: str
    project: Optional[str] = None
    similarity_score: float
    snippet: str

class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: List[KnowledgeSource] = []
    chapter_context: Optional[str] = None
    suggested_followups: List[str] = []

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 4
    category: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[KnowledgeSource]

class StoryChapter(BaseModel):
    id: str
    number: str
    title: str
    subtitle: str
    summary: str
    narration: str
    key_themes: List[str]
    projects_featured: List[str]
    suggested_questions: List[str]
    quote: Optional[str] = None
