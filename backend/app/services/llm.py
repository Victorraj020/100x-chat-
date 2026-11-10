import re
from typing import List, Dict, Any, Tuple
from ..config import settings

SYSTEM_PROMPT = """You are Victorraj, answering directly in the first person.

CRITICAL INSTRUCTIONS:
- Answer ONLY what the user specifically asked. Be direct, natural, and concise.
- If someone asks "What's your name?", reply simply: "My name is Victorraj."
- If someone asks "Where do you live?", reply: "I'm based in India."
- If someone asks "What did you study?", reply: "I completed my BSc in Information Technology and I am currently doing my MSc in Computer Science."
- DO NOT dump your entire resume, philosophy, or background unless the user specifically asks for it.
- Keep answers short and human: 1-3 sentences maximum.
- Never use robotic prefixes like "Regarding X:".
"""

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.client = None
        self._init_client()

    def _init_client(self):
        if settings.GEMINI_API_KEY:
            try:
                from google import genai
                self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
                self.provider = "gemini_new"
                return
            except Exception as e:
                pass

            try:
                import google.generativeai as legacy_genai
                legacy_genai.configure(api_key=settings.GEMINI_API_KEY)
                self.client = legacy_genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=SYSTEM_PROMPT
                )
                self.provider = "gemini_legacy"
                return
            except Exception as e:
                pass

        if settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.provider = "openai"
                return
            except Exception as e:
                pass

        self.provider = "fallback"

    async def generate_response(
        self,
        user_message: str,
        retrieved_sources: List[Dict[str, Any]],
        conversation_history: str,
        chapter_context: str = None
    ) -> Tuple[str, List[str]]:
        context_str = self._format_retrieved_context(retrieved_sources)
        prompt = f"""PORTFOLIO FACTS:
{context_str}

CONVERSATION HISTORY:
{conversation_history}

INTERVIEWER:
"{user_message}"

INSTRUCTIONS:
- Answer ONLY what was asked as Victorraj.
- Be concise (1-2 sentences). Do not over-explain.
- Output 2 short follow-up questions at the end:
FOLLOW_UPS:
- [Question 1]
- [Question 2]
"""

        # 1. Try Gemini New
        if self.provider == "gemini_new" and self.client:
            try:
                from google.genai import types
                response = self.client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.5,
                    )
                )
                if response and response.text:
                    return self._parse_llm_output(response.text)
            except Exception as e:
                pass

        # 2. Try Gemini Legacy
        if self.provider == "gemini_legacy" and self.client:
            try:
                response = self.client.generate_content(prompt)
                if response and response.text:
                    return self._parse_llm_output(response.text)
            except Exception as e:
                pass

        # 3. Try OpenAI
        if self.provider == "openai" and self.client:
            try:
                response = self.client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                )
                text = response.choices[0].message.content
                if text:
                    return self._parse_llm_output(text)
            except Exception as e:
                pass

        # 4. Direct, crisp fallback responder
        return self._generate_crisp_direct_response(user_message, retrieved_sources, conversation_history)

    def _format_retrieved_context(self, sources: List[Dict[str, Any]]) -> str:
        if not sources:
            return ""
        return "\n".join(f"- [{s['id']}] {s['title']}: {s['content']}" for s in sources)

    def _parse_llm_output(self, raw_text: str) -> Tuple[str, List[str]]:
        follow_ups = []
        if "FOLLOW_UPS:" in raw_text:
            parts = raw_text.split("FOLLOW_UPS:")
            main_text = parts[0].strip()
            for line in parts[1].strip().split("\n"):
                clean = line.strip().lstrip("-*123456789. ")
                if clean:
                    follow_ups.append(clean)
        else:
            main_text = raw_text.strip()
            follow_ups = [
                "Tell me more about QFoundry.",
                "What is your approach to Generative AI?"
            ]
        return main_text, follow_ups[:2]

    def _generate_crisp_direct_response(
        self,
        query: str,
        sources: List[Dict[str, Any]],
        history: str
    ) -> Tuple[str, List[str]]:
        """
        Direct, precise answers that answer exactly what was asked without fluff.
        """
        q = query.strip().lower()
        hist = history.lower()

        # 1. Name
        if any(w in q for w in ["your name", "ur name", "who are you", "what is your name", "whats your name"]):
            return (
                "My name is Victorraj.",
                [
                    "What is your background?",
                    "What projects have you built?"
                ]
            )

        # 2. Greetings
        if q in ["hi", "hello", "hey", "hi there", "hello there"]:
            return (
                "Hi! I'm Victorraj. How can I help you today?",
                [
                    "Tell me about your background.",
                    "What projects have you built?"
                ]
            )

        # 3. Location / Address / Where do you live
        if any(w in q for w in ["address", "where do you live", "location", "where are you from", "where are you based"]):
            return (
                "I am based in India.",
                [
                    "What are you currently studying?",
                    "What projects have you built?"
                ]
            )

        # 4. Education / Studies / Degree
        if any(w in q for w in ["study", "degree", "education", "college", "university", "msc", "bsc", "school"]):
            return (
                "I completed my BSc in Information Technology and I am currently pursuing my MSc in Computer Science.",
                [
                    "Why did you choose Computer Science?",
                    "What projects have you built?"
                ]
            )

        # 5. Background / Life story / Tell me about yourself
        if any(w in q for w in ["life story", "your journey", "your story", "tell me about yourself", "tell me about ur self", "your background", "introduce yourself"]):
            return (
                "After completing my BSc in Information Technology, I chose to pursue an MSc in Computer Science to understand how systems work from first principles. "
                "I'm an independent builder at heart—when I struggled to understand quantum circuits, I built QFoundry to visualize them, then wrote a pure TypeScript simulation engine from scratch, and have since focused on building reliable Generative AI systems.",
                [
                    "What’s your #1 superpower?",
                    "What are the top 3 areas you’d like to grow in?"
                ]
            )

        # 5b. #1 Superpower
        if any(w in q for w in ["superpower", "super power", "#1 strength", "greatest strength", "best quality"]):
            return (
                "My #1 superpower is independent learning and fearless experimentation. I am completely comfortable entering unfamiliar domains without a roadmap, making mistakes, and figuring things out by building working software from scratch.",
                [
                    "How do you push your boundaries and limits?",
                    "What are the top 3 areas you’d like to grow in?"
                ]
            )

        # 5c. Top 3 areas to grow in
        if any(w in q for w in ["areas you’d like to grow", "areas you'd like to grow", "areas to grow", "top 3 areas", "grow in", "want to grow"]):
            return (
                "The top 3 areas I want to grow in are: 1. Deepening my theoretical and mathematical foundations in machine learning. 2. Mastering production-grade evaluation and latency/hallucination benchmarking for AI systems. 3. Collaborating on large-scale distributed engineering systems.",
                [
                    "What misconception do your coworkers have about you?",
                    "What is your #1 superpower?"
                ]
            )

        # 5d. Misconception coworkers have
        if any(w in q for w in ["misconception", "misunderstood", "coworkers", "colleagues", "think about you"]):
            return (
                "Because I enjoy diving deep into independent problem-solving and building systems on my own, people sometimes assume I prefer working in isolation. In reality, I thrive on collaborative architectural discussions, pair programming, and learning from other experienced engineers.",
                [
                    "How do you push your boundaries and limits?",
                    "What kind of team brings out your best work?"
                ]
            )

        # 5e. Pushing boundaries and limits
        if any(w in q for w in ["push your boundaries", "push your limits", "boundaries and limits", "push boundaries", "comfort zone"]):
            return (
                "I push my boundaries by deliberately choosing problems where I don't know the solution beforehand. For example, building a 16-qubit quantum simulator in pure TypeScript forced me to learn complex-number linear algebra from scratch rather than taking the easy route of using existing frameworks.",
                [
                    "What was the hardest part of building QFoundry npm?",
                    "What is your approach to Generative AI engineering?"
                ]
            )

        # 6. What is QFoundry / Why did you build it
        if "qfoundry" in q:
            if any(w in q for w in ["npm", "simulator", "engine", "typescript", "without", "zero"]):
                return (
                    "QFoundry npm is an independent quantum simulation engine I built from scratch in TypeScript with zero dependencies, capable of simulating up to 16 qubits.",
                    [
                        "What was the hardest part of building it?",
                        "How does it differ from Qiskit?"
                    ]
                )
            return (
                "QFoundry is a VS Code extension I built to visualize quantum circuits and state vectors in real time, built with React and Qiskit.",
                [
                    "Why did you build it?",
                    "Tell me about QFoundry npm."
                ]
            )

        # 7. What is Vic-NLP
        if "vic-nlp" in q or "vic nlp" in q:
            return (
                "Vic-NLP is a local AI assistant project I built in Python to explore multi-layer context routing and structured knowledge retrieval with local Llama models.",
                [
                    "How did you implement context routing?",
                    "What did you learn from it?"
                ]
            )

        # 8. What is AuraSync
        if "aurasync" in q or "fashion" in q:
            return (
                "AuraSync AI is a fashion recommendation web app built with Next.js, FastAPI, Supabase, and the Gemini API for visual and multimodal analysis.",
                [
                    "What was your role in AuraSync?",
                    "What tech stack did you use?"
                ]
            )

        # 9. What is NeuroVoice
        if "neurovoice" in q or "parkinson" in q:
            return (
                "NeuroVoice AI was an exploratory research project where I tested ML and PennyLane quantum ML models on acoustic voice features for Parkinson's risk screening.",
                [
                    "What was the research scope?",
                    "What ML models did you use?"
                ]
            )

        # 10. How is this chatbot / app made
        if any(w in q for w in ["chatbot made of", "chatbot built", "how is this built", "what is this app", "tech stack"]):
            return (
                "This chatbot is built with Next.js 16 and TypeScript on the frontend (hosted on Netlify), and FastAPI with an in-memory RAG vector store on the backend (hosted on Render).",
                [
                    "How does the voice feature work?",
                    "How does the RAG pipeline work?"
                ]
            )

        # 11. Career plans / Future / What are you looking for
        if any(w in q for w in ["career", "future", "goals", "further in your career", "role", "looking for"]):
            return (
                "I am looking for a role as a Generative AI Engineer or Full-Stack Developer where I can build and evaluate end-to-end AI applications.",
                [
                    "What areas of AI are you focusing on?",
                    "What are your core technical skills?"
                ]
            )

        # 12. Strengths / Weaknesses
        if any(w in q for w in ["strength", "weakness"]):
            if "weakness" in q or "improve" in q or "grow" in q:
                return (
                    "I am actively working on deepening my mathematical ML theory and refining production-grade evaluation frameworks for LLMs.",
                    [
                        "What are your main strengths?",
                        "How do you approach learning new technologies?"
                    ]
                )
            return (
                "My core strengths are independent learning, curiosity, hands-on building, and persistence when solving unfamiliar technical problems.",
                [
                    "What areas are you actively working to improve?",
                    "Can you give an example of an unfamiliar problem you solved?"
                ]
            )

        # 13. Follow-up: "tell me more" / "lesson"
        if any(w in q for w in ["tell me more", "could you tell me more", "lesson", "rewarding"]):
            if "vic-nlp" in hist:
                return (
                    "The key lesson was context engineering: a model is only as good as the context you feed it. Layered routing helped prevent hallucinations.",
                    ["How does that connect to your RAG approach?", "Tell me about AuraSync."]
                )
            elif "qfoundry" in hist:
                return (
                    "The biggest takeaway was breaking down complex linear algebra into code step-by-step rather than relying on external libraries.",
                    ["How does QFoundry npm work?", "What are your career goals?"]
                )
            return (
                "I find I learn best by building practical tools to solve problems I face, rather than just reading documentation.",
                ["What project are you most proud of?", "What are you working on next?"]
            )

        # 14. Fallback to top source content in 1 clean sentence
        if sources:
            clean = sources[0]['content'].replace("\n", " ").strip()
            sentence = clean.split(". ")[0] + "."
            return (
                sentence,
                [
                    "Could you tell me more about that?",
                    "What other projects have you built?"
                ]
            )

        return (
            "I'm Victorraj. Feel free to ask me anything about my projects, technical stack, or background.",
            [
                "What projects have you built?",
                "What is your background?"
            ]
        )

llm_service = LLMService()
