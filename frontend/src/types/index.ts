export interface KnowledgeSource {
  id: string;
  title: string;
  category: string;
  project?: string;
  similarity_score: number;
  snippet: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: KnowledgeSource[];
  suggested_followups?: string[];
  timestamp: string;
}

export interface StoryChapter {
  id: string;
  number: string;
  title: string;
  subtitle: string;
  summary: string;
  narration: string;
  key_themes: string[];
  projects_featured: string[];
  suggested_questions: string[];
  quote?: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  sources: KnowledgeSource[];
  chapter_context?: string;
  suggested_followups: string[];
}
