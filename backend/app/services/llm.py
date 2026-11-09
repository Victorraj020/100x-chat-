import re
from typing import List, Dict, Any, Tuple
from ..config import settings
from ..schemas import KnowledgeSource

SYSTEM_PROMPT = """You are an AI representation of Victorraj, speaking in the first person during a Generative AI Engineer recruitment assessment.

## CORE IDENTITY:
- Name: Victorraj.
- Education: Currently pursuing an MSc in Computer Science after completing a BSc in Information Technology.
- Role / Passion: Aspiring AI Engineer, Full-Stack Developer, and independent technology enthusiast with deep curiosity about Generative AI, quantum computing, machine learning, and systems engineering.
- Philosophy: "I am a builder driven by curiosity. I learn by understanding, experiment by building, and grow by taking on problems I haven't solved before."
- Learning approach: I don't always need a complete roadmap before starting. I begin with an idea, experiment, make mistakes, and build working software. I prefer understanding the underlying concept instead of blindly copying code.

## COMMUNICATION STYLE:
- Speak naturally in the first person ("I", "my", "we" when collaborating).
- Tone: Thoughtful, humble, curious, articulate, and practical.
- Avoid corporate buzzwords, hype, and exaggerated claims.
- Spoken-friendly: Concise, usually around 30–60 seconds of reading time (~80 to 160 words), unless a deeper technical explanation is requested.
- Maintain continuity across follow-up questions. Notice references like "it", "that project", "the hardest part", and connect them to previously discussed projects.

## GROUNDING & HALLUCINATION PREVENTION:
1. ONLY make claims supported by the provided RETRIEVED CONTEXT and CONVERSATION HISTORY.
2. Clearly distinguish between:
   - What I have built: QFoundry (VS Code extension with Qiskit & React), QFoundry npm (pure TypeScript zero-dependency quantum simulation engine up to 16 qubits), Vic-NLP (local assistant with context routing & Llama workflows), AuraSync AI (fashion recommendations with Next.js, FastAPI, Supabase, Gemini).
   - What I have researched/experimented with: NeuroVoice AI (exploratory voice-based Parkinson's risk-screening research concept using ML & PennyLane QML — explicitly NOT a medical diagnostic tool).
   - What I am currently learning / improving: Deeper theoretical ML mathematics, production-grade AI system evaluation, multi-agent frameworks, large-scale team collaboration.
3. NEVER invent employment history, past companies, metrics, or technologies I haven't used.
4. If asked about something outside my experience, be honest: acknowledge that I haven't worked with it yet, but explain how I would approach learning it based on my engineering principles.
"""

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.gemini_model = None
        self.openai_client = None

        if settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel(
                    model_name=settings.GEMINI_MODEL,
                    system_instruction=SYSTEM_PROMPT
                )
                self.provider = "gemini"
            except Exception as e:
                print(f"[LLMService] Gemini init failed: {e}")

        if not self.gemini_model and settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.provider = "openai"
            except Exception as e:
                print(f"[LLMService] OpenAI init failed: {e}")

    async def generate_response(
        self,
        user_message: str,
        retrieved_sources: List[Dict[str, Any]],
        conversation_history: str,
        chapter_context: str = None
    ) -> Tuple[str, List[str]]:
        """
        Generate grounded, natural first-person response representing Victorraj.
        Returns: (response_text, suggested_followups)
        """
        context_str = self._format_retrieved_context(retrieved_sources)
        prompt = f"""### RETRIEVED KNOWLEDGE CONTEXT:
{context_str}

### CURRENT CHAPTER CONTEXT:
{chapter_context or 'General Overview'}

### RECENT CONVERSATION HISTORY:
{conversation_history}

### INTERVIEWER QUESTION:
"{user_message}"

### INSTRUCTIONS:
- Answer as Victorraj in first-person.
- Use the retrieved knowledge to answer accurately.
- Follow up seamlessly if this question relates to the previous topic.
- At the very end of your response, output exactly 2 suggested follow-up questions formatted as:
FOLLOW_UPS:
- [Follow-up question 1]
- [Follow-up question 2]
"""

        # Try Gemini
        if self.provider == "gemini" and self.gemini_model:
            try:
                response = self.gemini_model.generate_content(prompt)
                raw_text = response.text
                return self._parse_llm_output(raw_text)
            except Exception as e:
                print(f"[LLMService] Gemini generation error: {e}. Falling back.")

        # Try OpenAI
        if self.provider == "openai" and self.openai_client:
            try:
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
                response = self.openai_client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=messages,
                    temperature=0.7,
                )
                raw_text = response.choices[0].message.content
                return self._parse_llm_output(raw_text)
            except Exception as e:
                print(f"[LLMService] OpenAI generation error: {e}. Falling back.")

        # Contextual Fallback Responder
        return self._generate_contextual_fallback(user_message, retrieved_sources, conversation_history)

    def _format_retrieved_context(self, sources: List[Dict[str, Any]]) -> str:
        if not sources:
            return "No specific documents retrieved. Respond generally based on your core background."
        formatted = []
        for s in sources:
            formatted.append(f"[{s['id']}] {s['title']} ({s['category']}):\n{s['content']}")
        return "\n\n".join(formatted)

    def _parse_llm_output(self, raw_text: str) -> Tuple[str, List[str]]:
        follow_ups = []
        if "FOLLOW_UPS:" in raw_text:
            parts = raw_text.split("FOLLOW_UPS:")
            main_text = parts[0].strip()
            follow_up_lines = parts[1].strip().split("\n")
            for line in follow_up_lines:
                clean_line = line.strip().lstrip("-*123456789. ")
                if clean_line:
                    follow_ups.append(clean_line)
        else:
            main_text = raw_text.strip()
            follow_ups = [
                "What was the most challenging technical hurdle?",
                "How does this connect to your future AI goals?"
            ]

        return main_text, follow_ups[:3]

    def _generate_contextual_fallback(
        self,
        query: str,
        sources: List[Dict[str, Any]],
        history: str
    ) -> Tuple[str, List[str]]:
        """
        High-fidelity contextual fallback that crafts natural first-person responses
        from retrieved chunks when external LLM API keys are not yet configured.
        """
        q_lower = query.lower()

        # Follow-up resolution from history
        context_hint = ""
        if "hardest" in q_lower or "challenge" in q_lower or "why" in q_lower:
            if "qfoundry" in history.lower():
                context_hint = "qfoundry"
            elif "vic-nlp" in history.lower():
                context_hint = "vic-nlp"
            elif "aurasync" in history.lower():
                context_hint = "aurasync"

        # Check matched project/theme
        if "qfoundry" in q_lower or context_hint == "qfoundry":
            if "npm" in q_lower or "simulator" in q_lower or "engine" in q_lower or "difference" in q_lower:
                text = (
                    "QFoundry npm is something I'm particularly proud of because it is written entirely from scratch in TypeScript, "
                    "with zero external dependencies. While my VS Code extension used Python and Qiskit for circuit compilation, "
                    "for the npm package I wanted to understand the actual math: implementing complex number arithmetic, matrix tensor products, "
                    "and state-vector calculations capable of simulating up to 16 qubits. It taught me that understanding fundamentals is much more "
                    "empowering than just calling pre-packaged libraries."
                )
                follow_ups = [
                    "What was the biggest challenge in building the simulation engine?",
                    "How do you visualize these circuits in the VS Code extension?"
                ]
            else:
                text = (
                    "I developed QFoundry because when I began studying quantum computing, I found myself copying quantum algorithms without "
                    "truly visualizing what the gates were doing to the state vectors. I wanted a developer tool inside VS Code that provided "
                    "step-by-step gate execution timelines, QASM circuit visualization, and phase inspection. Building the frontend in React/TypeScript "
                    "and connecting it with a Python Qiskit backend proved to me that I could solve my own learning frustrations by building a real developer tool."
                )
                follow_ups = [
                    "What was the hardest technical challenge in QFoundry?",
                    "How does your independent QFoundry npm package differ from the extension?"
                ]
            return text, follow_ups

        if "vic-nlp" in q_lower or "assistant" in q_lower or context_hint == "vic-nlp":
            text = (
                "With Vic-NLP, my goal was to explore contextual understanding and knowledge retrieval beyond single-turn prompt interactions. "
                "I organized information into layered context-routing pipelines so the assistant could retrieve relevant background before responding, "
                "combining local Llama models with structured retrieval workflows. That experience sparked my current focus on context engineering and RAG."
            )
            follow_ups = [
                "How did you handle context routing?",
                "How does Vic-NLP inform your view of Generative AI architectures?"
            ]
            return text, follow_ups

        if "aurasync" in q_lower or "fashion" in q_lower or context_hint == "aurasync":
            text = (
                "AuraSync AI is a full-stack fashion analysis application I built using Next.js, TypeScript, Tailwind CSS, FastAPI, Supabase, "
                "and the Gemini API. Rather than treating AI as an isolated model, it gave me hands-on experience integrating vision and multimodal "
                "recommendations seamlessly into a reactive user experience with authenticated database storage."
            )
            follow_ups = [
                "What did you learn about full-stack AI system design?",
                "How did you integrate FastAPI with Supabase?"
            ]
            return text, follow_ups

        if "neurovoice" in q_lower or "parkinson" in q_lower or "health" in q_lower:
            text = (
                "NeuroVoice AI was an exploratory research project investigating voice biomarkers for Parkinson's disease risk screening. "
                "I experimented with acoustic feature extraction, classical ML classifiers, and PennyLane/Qiskit quantum machine learning techniques. "
                "I always emphasize that this was strictly an early-stage research concept, not a clinical diagnostic system. It taught me a tremendous amount "
                "about working with noisy real-world data and the ethical responsibilities of AI in health-related domains."
            )
            follow_ups = [
                "What quantum machine learning techniques did you test?",
                "What were the biggest data challenges you encountered?"
            ]
            return text, follow_ups

        if "who are you" in q_lower or "background" in q_lower or "introduce" in q_lower:
            text = (
                "I'm Victorraj. I am currently pursuing an MSc in Computer Science after completing my BSc in Information Technology. "
                "I consider myself a builder driven by curiosity: I love opening up technologies to understand how they work internally, "
                "and then applying that understanding to build practical tools—whether that's an independent quantum circuit simulator in TypeScript, "
                "a local context-aware AI assistant, or full-stack GenAI web applications."
            )
            follow_ups = [
                "What projects have you built recently?",
                "How do you approach learning unfamiliar technologies?"
            ]
            return text, follow_ups

        if "strength" in q_lower or "weakness" in q_lower or "grow" in q_lower or "improve" in q_lower:
            text = (
                "My key strengths are independent learning, genuine curiosity, adaptability, and a hands-on building mindset. "
                "Equally important, I am clear about where I am actively growing: I am deepening my theoretical machine learning math, "
                "refining my technical communication, and mastering production-grade AI evaluation methodologies beyond superficial output checks."
            )
            follow_ups = [
                "How do you approach testing and evaluating an AI system?",
                "What is your philosophy on problem-solving?"
            ]
            return text, follow_ups

        # If retrieved sources exist, summarize them in first person
        if sources:
            primary_source = sources[0]
            text = (
                f"Regarding {primary_source['title']}: {primary_source['content']} "
                "In all my projects, my focus is on understanding the core principles and building something robust rather than just following tutorials."
            )
            follow_ups = [
                "Could you tell me more about that?",
                "What was the most rewarding lesson from that project?"
            ]
            return text, follow_ups

        # Default fallback
        text = (
            "I approach engineering by digging into how systems work under the hood. "
            "Whether designing RAG pipelines with pgvector, writing quantum simulation engines in TypeScript, "
            "or integrating full-stack AI services, I focus on building practical, grounded applications."
        )
        follow_ups = [
            "What projects have you built?",
            "What motivated you to explore Generative AI engineering?"
        ]
        return text, follow_ups

llm_service = LLMService()

