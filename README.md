# AI Chatbot — Context-Aware Voice Agent & Interactive Story

An interactive, production-quality AI voice chatbot and storytelling application designed for a **Generative AI Engineer recruitment assessment**, authentically representing **Victorraj**'s background, projects, engineering philosophy, and career ambitions.

Built with an editorial aesthetic: dark charcoal canvas, warm white typography, cinematic chapter transitions, Web Speech API voice synthesis and speech recognition, coupled with a grounded Retrieval-Augmented Generation (RAG) backend.

---

## 1. System Architecture

```mermaid
flowchart TD
    User["Interviewer (Voice / Text)"] -->|Audio / Text Query| Frontend["Next.js 16 Editorial Frontend"]
    
    subgraph Frontend_Layer ["Frontend (Next.js 16 + Tailwind CSS)"]
        Hero["Opening Screen: 'Every journey starts with a question'"]
        Story["Interactive Story Mode (5 Chapters)"]
        VoiceIO["Web Speech Recognition & Synthesis"]
        ChatModal["Conversational Drawer & RAG Citations Inspector"]
    end
    
    Frontend -->|POST /api/chat (query, session_id, context)| Backend["FastAPI Backend (Python 3.12)"]
    
    subgraph Backend_Layer ["Backend (FastAPI & RAG Pipeline)"]
        Router["API Router (/api/chat, /api/story, /api/knowledge)"]
        Memory["Conversation Memory Buffer (Session Coreference)"]
        Embedding["Embedding Service (Gemini / OpenAI / Deterministic)"]
        VectorDB[("Vector Store: pgvector / Cosine In-Memory")]
        Knowledge["Structured Knowledge Base (13 Canonical Chunks)"]
        LLM["LLM Generation Layer (Gemini 2.5 / GPT-4o-mini / Fallback)"]
    end
    
    Knowledge -->|Ingest & Embed| VectorDB
    Router -->|Query| Embedding
    Embedding -->|Dense Vector| VectorDB
    VectorDB -->|Ranked Chunks + Scores| LLM
    Memory -->|Recent Turns| LLM
    LLM -->|Grounded First-Person Answer + Follow-ups| Frontend
```

---

## 2. Key Features

### 📖 Interactive Story Mode
- **Cinematic Chapters**:
  - **Chapter 01 — The Beginning**: Educational transition from BSc in IT to MSc in Computer Science, discovering internal mechanics.
  - **Chapter 02 — The Builder**: QFoundry (VS Code Extension), QFoundry npm (pure TypeScript zero-dependency quantum simulation engine up to 16 qubits), Vic-NLP, AuraSync AI, and NeuroVoice AI.
  - **Chapter 03 — Exploring Intelligence**: Moving beyond API wrappers into complete AI systems (RAG, pgvector, context routing, evaluation, quantum ML).
  - **Chapter 04 — The Thinking Process**: Comfort in unfamiliar domains, building without a rigid roadmap, learning through implementation, and debugging root causes.
  - **Chapter 05 — Beyond Today**: Career ambitions as a Generative AI Engineer, theoretical ML growth, and reliable system design.
- **Narration Audio**: Built-in speech synthesis allowing interviewers to listen to each chapter's narration with live audio wave indicators.
- **Interactive Project Cards**: One-click navigation to code repositories, live demos, and direct "Ask AI about this" prompts.

### 🎙️ Conversational Voice & Text Interface
- **Voice-First Input**: Uses the browser's Web Speech API (`webkitSpeechRecognition`) for microphone input with live status indicator and sound wave pulse animation.
- **Natural Voice Playback**: AI responses are vocalized with high-quality browser speech synthesis, featuring an active audio indicator and instant "Stop Speaking" controls.
- **Contextual Memory & Follow-ups**: Seamlessly resolves ambiguous follow-up questions (e.g. asking *"Why did you build QFoundry?"* followed by *"What was the hardest part?"* maintains continuity).
- **RAG Citations & Hallucination Prevention Inspector**: Every response includes an expandable audit drawer displaying the exact retrieved knowledge chunks, source categories, and cosine similarity match scores.
- **Dynamic Suggested Prompts**: Provides 2–3 contextual follow-up questions after every turn.

---

## 3. Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | Next.js 16, React 19, TypeScript, Tailwind CSS, Lucide Icons, Web Speech API |
| **Backend** | Python 3.12, FastAPI, Pydantic, Uvicorn, NumPy, AsyncPG, pgvector |
| **Generative AI** | Google Gemini API (`gemini-2.5-flash`), OpenAI API (`gpt-4o-mini`), Modular Fallback Engine |
| **Vector Database** | PostgreSQL with `pgvector` (Supabase / Neon), Automatic In-Memory Cosine Vector Store fallback |
| **Deployment** | Render (Frontend & Backend), Supabase (PostgreSQL), Cloudflare (Edge Security) |

---

## 4. Quick Start (Local Development)

### Prerequisites
- Node.js 18+ (tested on Node 24)
- Python 3.10+ (tested on Python 3.12)

### 1. Clone & Set Up Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment and activate
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Copy environment variables
cp .env.example .env

# Start FastAPI backend server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
> The backend automatically initializes its vector store and starts on `http://127.0.0.1:8000`.

### 2. Set Up Frontend

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install dependencies (already included in repository)
npm install

# Start Next.js development server
npm run dev
```
> Open `http://localhost:3000` in your browser.

---

## 5. Environment Variables

### Backend (`backend/.env`)

```ini
PORT=8000
HOST=0.0.0.0
DEBUG=True

# LLM Providers (Optional - high-fidelity grounded contextual fallback active if unset)
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=gemini
GEMINI_MODEL=gemini-2.5-flash

# Database (Optional - Supabase / PostgreSQL with pgvector)
# When omitted, the built-in in-memory cosine vector store runs automatically.
DATABASE_URL=postgresql://user:password@host:5432/dbname
VECTOR_DIMENSION=768
TOP_K_RETRIEVAL=4
```

### Frontend (`frontend/.env.local`)

```ini
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 6. PostgreSQL + pgvector Migration (Supabase / Render)

When connecting a production PostgreSQL database with the `pgvector` extension:

1. Connect to your database using psql or Supabase SQL Editor.
2. Run the provided schema script in `backend/database/schema.sql`:
   ```sql
   \i backend/database/schema.sql
   ```
3. Set `DATABASE_URL` in your backend environment variables. The backend will automatically detect the database and route vector searches through the PostgreSQL HNSW index.

---

## 7. Hallucination Prevention & Guardrails

1. **Strict Context Grounding**: The LLM system prompt mandates answering only with facts retrieved from the canonical personal knowledge base.
2. **Distinct Capability Tiers**:
   - **Built**: QFoundry (VS Code extension with Qiskit/React), QFoundry npm (pure TypeScript zero-dependency quantum simulation engine), Vic-NLP, AuraSync AI.
   - **Researched / Exploratory**: NeuroVoice AI (Parkinson's risk-screening research concept using ML/QML — explicitly non-diagnostic).
   - **Actively Learning**: Deeper mathematical foundations of ML, production LLM evaluation, multi-agent frameworks.
3. **No Fabricated History**: Never invents employment history, company affiliations, metrics, or achievements.
4. **Transparent Citations**: Interviewers can open the citation inspector on any message to verify the similarity score and original text snippet.

