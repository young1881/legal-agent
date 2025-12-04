from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    agent_type: str = "consultant"  # consultant, exam, chat


class Citation(BaseModel):
    source_id: str
    article_name: str
    section: Optional[str] = None
    content: str
    url: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
    sources: List[Dict[str, Any]]


class DocumentChunk(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]

