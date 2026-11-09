from typing import Dict, List, Optional
from datetime import datetime
from ..schemas import Message

class ConversationMemory:
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
        self.session_last_topics: Dict[str, str] = {}

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        self.sessions[session_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Keep within max_turns * 2 (user + assistant pairs)
        if len(self.sessions[session_id]) > self.max_turns * 2:
            self.sessions[session_id] = self.sessions[session_id][-(self.max_turns * 2):]

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        return self.sessions.get(session_id, [])

    def format_history_for_prompt(self, session_id: str) -> str:
        history = self.get_history(session_id)
        if not history:
            return "No previous conversation."
        
        formatted = []
        for msg in history[-8:]: # Last 4 turns
            role_label = "Interviewer" if msg["role"] == "user" else "Victorraj (AI)"
            formatted.append(f"{role_label}: {msg['content']}")
        return "\n".join(formatted)

    def set_active_topic(self, session_id: str, topic: str):
        self.session_last_topics[session_id] = topic

    def get_active_topic(self, session_id: str) -> Optional[str]:
        return self.session_last_topics.get(session_id)

    def clear(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.session_last_topics:
            del self.session_last_topics[session_id]

conversation_memory = ConversationMemory()

