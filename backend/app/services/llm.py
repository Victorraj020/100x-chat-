import re
import random
from typing import List, Dict, Any, Tuple
from ..config import settings
from ..schemas import KnowledgeSource

SYSTEM_PROMPT = """You are Victorraj, speaking naturally in the first person during a Generative AI Engineer interview/assessment.

## CORE IDENTITY:
- Name: Victorraj.
- Education: Currently pursuing an MSc in Computer Science after completing a BSc in Information Technology.
- Mindset: A builder driven by curiosity. You learn by understanding the mechanics, experiment by building practical software, and grow by tackling problems you haven't solved before.
- Philosophy: You don't always need a complete roadmap before starting. You prefer understanding underlying concepts over blindly copying tutorials.

## COMMUNICATION STYLE:
- Always speak naturally in first person ("I", "my").
- Sound human, thoughtful, humble, conversational, and direct.
- DO NOT speak like a database query or say things like "Regarding X:". Talk like you are in a friendly conversation with an interviewer.
- Be concise (approx 50-100 words), focused on the user's specific question.
- Seamlessly follow up if the user asks "tell me more", "how so?", "why?", or references previous topics.

## PROJECTS YOU BUILT:
- QFoundry (VS Code extension for quantum circuit visualization with Qiskit & React).
- QFoundry npm (pure TypeScript independent simulation engine up to 16 qubits with zero dependencies).
- Vic-NLP (local assistant with multi-layer context routing & Llama workflows).
- AuraSync AI (full-stack fashion recommendations using Next.js, FastAPI, Supabase, Gemini).
- NeuroVoice AI (exploratory voice Parkinson's risk screening concept with PennyLane QML — research concept, NOT medical).
"""

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.client = None
        self._init_client()

    def _init_client(self):
        # 1. Try modern google-genai SDK
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
                self.provider = "gemini_new"
                print("[LLMService] Initialized with modern google-genai client.")
                return
            except Exception as e:
                print(f"[LLMService] modern google-genai init failed: {e}")

            # 2. Try legacy google.generativeai SDK
            try:
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=settings.GEMINI_API_KEY)
                self.client = legacy_genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=SYSTEM_PROMPT
                )
                self.provider = "gemini_legacy"
                print("[LLMService] Initialized with legacy google.generativeai client.")
                return
            except Exception as e:
                print(f"[LLMService] legacy google.generativeai init failed: {e}")

        # 3. Try OpenAI if configured
        if settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.provider = "openai"
                print("[LLMService] Initialized with OpenAI client.")
                return
            except Exception as e:
                print(f"[LLMService] OpenAI init failed: {e}")

        self.provider = "fallback"

    async def generate_response(
        self,
        user_message: str,
        retrieved_sources: List[Dict[str, Any]],
        conversation_history: str,
        chapter_context: str = None
    ) -> Tuple[str, List[str]]:
        context_str = self._format_retrieved_context(retrieved_sources)
        prompt = f"""RETRIEVED FACTS FROM MY PORTFOLIO:
{context_str}

CHAPTER / CONTEXT:
{chapter_context or 'General'}

RECENT CONVERSATION HISTORY:
{conversation_history}

INTERVIEWER:
"{user_message}"

INSTRUCTIONS:
- Reply naturally in the first person as Victorraj.
- Sound conversational, friendly, and practical.
- Keep the response around 2-4 sentences unless detailed technical depth was specifically asked.
- Provide 2 natural follow-up questions at the very end in this format:
FOLLOW_UPS:
- [Question 1]
- [Question 2]
"""

        # Generation via modern google.genai
        if self.provider == "gemini_new" and self.client:
            try:
                from google.genai import types
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.7,
                    )
                )
                if response and response.text:
                    return self._parse_llm_output(response.text)
            except Exception as e:
                print(f"[LLMService] google-genai generation error: {e}")

        # Generation via legacy google.generativeai
        if self.provider == "gemini_legacy" and self.client:
            try:
                response = self.client.generate_content(prompt)
                if response and response.text:
                    return self._parse_llm_output(response.text)
            except Exception as e:
                print(f"[LLMService] legacy generation error: {e}")

        # Generation via OpenAI
        if self.provider == "openai" and self.client:
            try:
                response = self.client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                )
                text = response.choices[0].message.content
                if text:
                    return self._parse_llm_output(text)
            except Exception as e:
                print(f"[LLMService] OpenAI generation error: {e}")

        # Conversational Persona Engine (Human-sounding multi-turn dialog)
        return self._generate_conversational_persona_response(
            user_message, retrieved_sources, conversation_history, chapter_context
        )

    def _format_retrieved_context(self, sources: List[Dict[str, Any]]) -> str:
        if not sources:
            return "No specific documents retrieved."
        formatted = []
        for s in sources:
            formatted.append(f"- [{s['id']}] {s['title']}: {s['content']}")
        return "\n".join(formatted)

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
                "What was the hardest technical challenge in that project?",
                "How do you see that tying into Generative AI engineering?"
            ]
        return main_text, follow_ups[:2]

    def _generate_conversational_persona_response(
        self,
        query: str,
        sources: List[Dict[str, Any]],
        history: str,
        chapter_context: str
    ) -> Tuple[str, List[str]]:
        """
        Conversational Persona Engine:
        Provides dynamic, natural, human responses with memory of the ongoing conversation,
        avoiding repetitive templates, robotic prefixes, or looping answers.
        """
        q = query.strip().lower()
        hist = history.lower()

        # 1. Greetings & Pleasantries
        if q in ["hi", "hello", "hey", "hi there", "hello there", "good morning", "good afternoon"]:
            return (
                "Hey! Great to meet you. I'm Victorraj. Feel free to ask me anything about my background, "
                "my projects like QFoundry or Vic-NLP, or how I approach building full-stack and Generative AI systems.",
                [
                    "Tell me about yourself and your journey so far.",
                    "Why did you build QFoundry?",
                ]
            )

        # 2. Tell me about yourself / Name / Background
        if any(w in q for w in ["your name", "ur name", "who are you", "tell me about yourself", "tell me about ur self", "introduce yourself", "your background"]):
            return (
                "My name is Victorraj. I completed my BSc in Information Technology and am currently pursuing an MSc in Computer Science. "
                "I'm an aspiring AI Engineer and full-stack developer who loves exploring how systems work under the hood—from authoring quantum simulation engines in TypeScript to designing production RAG pipelines.",
                [
                    "Why did you decide to build QFoundry?",
                    "What is your approach to Generative AI engineering?",
                ]
            )

        # 2b. How this chatbot / app is built
        if any(w in q for w in ["chatbot made of", "chatbot built", "how is this built", "how this works", "tech stack", "what is this app", "architecture of this"]):
            return (
                "I designed and built this AI Voice Chatbot from scratch as a production RAG application. "
                "The frontend is built with Next.js 16 (App Router), TypeScript, Tailwind CSS v4, and the Web Speech API for real-time speech recognition and voice synthesis, hosted on Netlify. "
                "The backend is powered by Python and FastAPI, running on Render Cloud with an in-memory vector store computing cosine similarity over my portfolio knowledge base, and grounded by Gemini for reasoning.",
                [
                    "How does the RAG pipeline prevent hallucinations?",
                    "Why did you choose FastAPI over a serverless backend?"
                ]
            )

        # 2c. Contact / Location / Personal details
        if any(w in q for w in ["address", "where do you live", "location", "contact", "email", "phone", "hire", "reach you"]):
            return (
                "I'm based in India, currently completing my MSc in Computer Science. "
                "You can connect with me and explore my work directly on GitHub at github.com/Victorraj020 or reach out for engineering opportunities!",
                [
                    "What kind of roles are you currently looking for?",
                    "Tell me about your projects like QFoundry."
                ]
            )

        # 3. Follow-up: "tell me more" / "rewarding lesson" / "elaborate"
        if any(w in q for w in ["tell me more", "could you tell me more", "rewarding lesson", "most rewarding", "lesson from that"]):
            if "vic-nlp" in hist or "assistant" in hist or "context" in hist:
                return (
                    "The most rewarding lesson from Vic-NLP was realizing that a powerful model is only half the battle. "
                    "The real intelligence comes from context engineering—routing the user's intent to the right knowledge layer "
                    "so the model isn't hallucinating or answering in isolation. That realization is what steered me deeper into modern RAG pipelines.",
                    [
                        "How did you implement context routing in Vic-NLP?",
                        "What is your favorite project you've worked on so far?"
                    ]
                )
            elif "qfoundry" in hist or "quantum" in hist:
                return (
                    "The biggest takeaway from QFoundry was learning not to be intimidated by unfamiliar math or systems. "
                    "When I couldn't grasp quantum gates from tutorials alone, building the simulator gate-by-gate in TypeScript "
                    "and computing the state vectors manually demystified the whole topic for me.",
                    [
                        "How did you build the QFoundry npm simulator without dependencies?",
                        "What are you currently looking to improve in your engineering skills?"
                    ]
                )
            elif "aurasync" in hist or "fashion" in hist:
                return (
                    "Building AuraSync taught me the discipline of product engineering. Connecting a model to an API is quick, "
                    "but making an end-to-end web app with authentication, database state in Supabase, and multimodal image analysis "
                    "requires disciplined API contract design between FastAPI and Next.js.",
                    [
                        "What tech stack did you use for AuraSync?",
                        "How do you approach learning unfamiliar technologies?"
                    ]
                )
            else:
                return (
                    "I find the most rewarding part of engineering is turning a personal frustration into a working tool. "
                    "Whenever I run into something that feels like a 'black box', my instinct is to open it up, write code to simulate it, "
                    "and build an application that makes it clear for myself and others.",
                    [
                        "Can you tell me about a time an approach failed?",
                        "What kind of roles are you currently looking for?"
                    ]
                )

        # 4. QFoundry / Quantum
        if "qfoundry" in q or "quantum" in q:
            if any(w in q for w in ["npm", "simulator", "engine", "typescript", "without", "dependency"]):
                return (
                    "QFoundry npm is an independent quantum simulation engine I wrote from scratch in TypeScript with zero external dependencies. "
                    "While my VS Code extension relied on Qiskit, with the npm package I wanted to understand the underlying linear algebra: "
                    "implementing complex numbers, tensor matrix products, and state-vector simulation capable of handling up to 16 qubits.",
                    [
                        "What was the hardest math challenge in building it?",
                        "How does this relate to your interest in AI engineering?"
                    ]
                )
            return (
                "I started QFoundry because when I began learning quantum computing, I felt like I was blindly copying algorithms without "
                "visualizing what was happening to the quantum state. So I built a VS Code extension that renders interactive circuit diagrams, "
                "step-by-step gate execution timelines, and phase visualizers using React and Qiskit.",
                [
                    "How does your QFoundry npm package differ from the extension?",
                    "What did you learn about developer tooling while building it?"
                ]
            )

        # 5. Vic-NLP / Context / RAG
        if "vic-nlp" in q or "rag" in q or "context" in q or "assistant" in q:
            return (
                "With Vic-NLP, I wanted to move beyond single-turn chat wrappers. I built a multi-layer context routing pipeline that "
                "retrieves background knowledge and maintains conversational context before sending prompts to local Llama models. "
                "It really shaped my current philosophy: building reliable AI is mostly about context management, retrieval, and evaluation.",
                [
                    "What is your approach to RAG architectures?",
                    "How do you minimize hallucinations in AI systems?"
                ]
            )

        # 6. AuraSync / Full-Stack
        if "aurasync" in q or "fashion" in q or "full-stack" in q or "full stack" in q:
            return (
                "AuraSync is an AI fashion recommendation app I built with Next.js, TypeScript, FastAPI, Supabase, and Gemini. "
                "It was a great exercise in shipping a real product: handling image inputs, generating structured visual advice, "
                "and managing user data securely.",
                [
                    "What was the biggest architectural decision you made on AuraSync?",
                    "How did you integrate FastAPI with the Gemini API?"
                ]
            )

        # 7. NeuroVoice / Health
        if "neurovoice" in q or "parkinson" in q or "voice" in q:
            return (
                "NeuroVoice AI was an exploratory research project where I tested machine learning and PennyLane quantum ML models "
                "on acoustic voice features for Parkinson's disease risk screening. I always clarify that it's strictly an early research concept, "
                "not a diagnostic tool, but it gave me great experience dealing with real-world noisy audio datasets.",
                [
                    "What quantum machine learning techniques did you experiment with?",
                    "What did that project teach you about AI ethics?"
                ]
            )

        # 7b. Career Ambition / Taking it further in career / Future
        if any(w in q for w in ["career", "future", "goals", "further in your career", "where do you see yourself", "looking for"]):
            return (
                "My goal is to work as a Generative AI Engineer on impactful products. "
                "I want to focus on designing complete AI systems—combining robust retrieval-augmented generation, thoughtful context management, "
                "and system evaluation. Long term, I also want to explore the intersection of machine learning and quantum computing.",
                [
                    "What specific areas of AI are you focusing on mastering next?",
                    "What kind of team environment brings out your best work?"
                ]
            )

        # 8. Strengths, Weaknesses, Growth
        if any(w in q for w in ["strength", "weakness", "growth", "improve", "learning approach", "unfamiliar"]):
            return (
                "My biggest strength is that I'm comfortable diving into unfamiliar technical domains and learning through experimentation. "
                "Where I'm actively growing is deepening my mathematical ML foundations and getting better at production-grade AI system evaluation, "
                "so I can measure model performance systematically rather than just checking whether an answer looks plausible.",
                [
                    "How do you handle a bug or architecture failure when you have no roadmap?",
                    "What kind of team environment brings out your best work?"
                ]
            )

        # 9. Dynamic synthesis from top retrieved source without robotic prefixes
        if sources:
            best = sources[0]
            clean_content = best['content'].replace("\n", " ").strip()
            # Truncate to first 2-3 sentences if long
            sentences = re.split(r'(?<=[.!?]) +', clean_content)
            summary = " ".join(sentences[:3])
            return (
                f"{summary} That hands-on experience really reinforced my belief in building systems from first principles.",
                [
                    f"What was the most rewarding lesson from {best.get('project') or 'that project'}?",
                    "How do you plan to take that further in your career?"
                ]
            )

        # 10. Default natural statement
        return (
            "I'm passionate about engineering systems that solve practical problems. "
            "Whether that's writing simulation algorithms from scratch, designing RAG pipelines, or connecting full-stack web architectures, "
            "I focus on understanding the core principles and building something that actually works.",
            [
                "What project are you most proud of?",
                "What motivated you to specialize in Generative AI?"
            ]
        )

llm_service = LLMService()
