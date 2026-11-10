"""
Structured Personal Knowledge Base for Victorraj.
This serves as the canonical source of truth for the RAG pipeline.
"""

from typing import List, Dict, Any

KNOWLEDGE_CHUNKS: List[Dict[str, Any]] = [
    # --- Category: Personal & Identity ---
    {
        "id": "bio-01",
        "title": "Identity & Background Overview",
        "category": "Personal Background",
        "project": None,
        "content": (
            "My name is Victorraj. I am currently pursuing an MSc in Computer Science after completing my BSc in Information Technology. "
            "I am an aspiring AI Engineer, Full-Stack Developer, and independent technology enthusiast with a growing interest in Generative AI, "
            "quantum computing, machine learning, and research. "
            "I enjoy understanding how technologies work internally rather than simply learning how to use them. "
            "I prefer building practical applications, experimenting with unfamiliar technologies, and turning ideas into working products. "
            "I don't consider myself someone who knows everything. I am comfortable entering unfamiliar areas, learning what is necessary, "
            "experimenting, and figuring things out."
        ),
        "tags": ["education", "identity", "msc", "bsc", "background"]
    },
    {
        "id": "bio-02",
        "title": "Engineering Philosophy & Mindset",
        "category": "Thinking Process",
        "project": None,
        "content": (
            "My approach to technology is driven by curiosity and practical problem-solving. "
            "I prefer understanding the underlying concept instead of blindly copying code. "
            "When I encounter a problem, I try to understand why it exists before choosing a solution. "
            "I enjoy exploring technologies outside my existing comfort zone. "
            "I believe learning becomes more meaningful when I build something with what I learn. "
            "I don't always need a complete roadmap before starting. Sometimes I begin with an idea, explore the technology, "
            "make mistakes, and gradually understand how to implement it. "
            "I don't want to build projects just to add them to my resume; I want to create something useful."
        ),
        "tags": ["philosophy", "problem-solving", "learning", "mindset"]
    },
    {
        "id": "bio-03",
        "title": "Strengths and Personality",
        "category": "Strengths",
        "project": None,
        "content": (
            "My primary strengths are: "
            "1. Independent learning: I am comfortable exploring unfamiliar technologies and learning through hands-on implementation. "
            "2. Curiosity: I naturally question how systems work underneath the surface and how they could be improved. "
            "3. Building mindset: I prefer turning abstract ideas into functional, interactive projects. "
            "4. Adaptability: I enjoy working across different areas of software engineering and emerging technologies. "
            "5. Persistence: I am willing to experiment, debug thoroughly, and revisit an approach when it fails."
        ),
        "tags": ["strengths", "adaptability", "persistence", "curiosity"]
    },
    {
        "id": "bio-04",
        "title": "Areas of Active Growth and Improvement",
        "category": "Growth Areas",
        "project": None,
        "content": (
            "I recognise that I still have room to grow and view these as areas of active development: "
            "1. Developing deeper theoretical and mathematical foundations in AI and machine learning. "
            "2. Improving my ability to communicate complex technical ideas cleanly and concisely. "
            "3. Collaborating on larger-scale engineering projects and codebases. "
            "4. Deepening my understanding of production-grade AI system architecture and reliability. "
            "5. Developing structured methodologies for evaluating LLM systems beyond basic output inspection."
        ),
        "tags": ["growth", "learning-goals", "self-awareness", "limitations"]
    },
    {
        "id": "bio-05",
        "title": "Career Ambition & Generative AI Motivation",
        "category": "Career Goals",
        "project": None,
        "content": (
            "I am motivated by building technology that solves meaningful problems. "
            "I don't want to restrict myself to one framework or language. "
            "I am particularly drawn to Generative AI because it combines software engineering, reasoning, language models, "
            "information retrieval, and real product development. "
            "I also maintain a long-term interest in quantum computing and research, and want to explore the intersection of AI "
            "and emerging computational technologies. "
            "I want to design complete AI systems rather than just wrapping API endpoints."
        ),
        "tags": ["career", "genai", "motivation", "quantum", "ambition"]
    },
    {
        "id": "bio-06",
        "title": "#1 Superpower and Pushing Boundaries",
        "category": "Strengths",
        "project": None,
        "content": (
            "My #1 superpower is independent learning and fearless experimentation: I am completely comfortable entering unfamiliar domains without a roadmap, making mistakes, and figuring things out by building working software. "
            "I push my boundaries and limits by deliberately choosing projects outside my comfort zone where I don't know the solution beforehand, such as writing a zero-dependency 16-qubit quantum simulator in pure TypeScript from scratch."
        ),
        "tags": ["superpower", "boundaries", "limits", "learning", "experimentation"]
    },
    {
        "id": "bio-07",
        "title": "Workplace Collaboration & Coworker Misconceptions",
        "category": "Working Style",
        "project": None,
        "content": (
            "Common misconception: Because I am deeply self-driven and enjoy diving into independent problem-solving and building projects from scratch, people sometimes assume I prefer working in isolation. "
            "In reality, I thrive on collaborative architectural discussions, pair programming, and learning from other experienced engineers on larger team initiatives."
        ),
        "tags": ["misconceptions", "collaboration", "teamwork", "coworkers", "communication"]
    },

    # --- Category: Projects ---
    {
        "id": "proj-qfoundry-01",
        "title": "QFoundry — Quantum Computing Development Tool (VS Code Extension)",
        "category": "Projects",
        "project": "QFoundry",
        "content": (
            "QFoundry (GitHub: https://github.com/Victorraj020/QFoundry, Website: https://qfoundry.netlify.app/) is a developer tool "
            "and VS Code extension I developed to help learners and developers understand what is happening inside quantum algorithms. "
            "When I initially studied quantum computing, I struggled to find resources explaining the internal mechanics of quantum circuits. "
            "I felt learners were simply copying algorithm code without visual intuition. "
            "Features include: Quantum circuit visualization, QASM circuit visualization, a gate-by-gate execution timeline, "
            "gate documentation and explanations, state-vector analysis, phase visualization, and local simulation. "
            "Tech stack: TypeScript and React frontend extension interface, integrated with a Python and Qiskit backend for circuit analysis."
        ),
        "tags": ["qfoundry", "quantum", "vscode-extension", "typescript", "react", "python", "qiskit"]
    },
    {
        "id": "proj-qfoundry-npm-01",
        "title": "QFoundry npm — Independent Quantum Simulation Engine",
        "category": "Projects",
        "project": "QFoundry npm",
        "content": (
            "QFoundry npm (npm: https://www.npmjs.com/package/qfoundry) is an independent quantum circuit simulator written entirely in TypeScript. "
            "Unlike my QFoundry VS Code extension which leverages Qiskit for circuit analysis, this package is an independent simulation engine "
            "built completely from scratch in TypeScript, without Python or external runtime dependencies. "
            "It implements: Quantum circuit construction, state-vector simulation, quantum gates, controlled operations, complex number arithmetic, "
            "and matrix calculations, supporting circuits up to 16 qubits. "
            "This project illustrates my interest in understanding the mathematical and algorithmic foundations behind technologies "
            "rather than relying entirely on third-party frameworks."
        ),
        "tags": ["qfoundry-npm", "quantum-simulator", "typescript", "math", "state-vector", "zero-dependencies"]
    },
    {
        "id": "proj-vicnlp-01",
        "title": "Vic-NLP — Local AI Assistant & Context Management",
        "category": "Projects",
        "project": "Vic-NLP",
        "content": (
            "Vic-NLP is a Python-based local AI assistant project focused on contextual understanding and knowledge retrieval. "
            "The goal was organizing information into multiple context-processing layers so the assistant could retrieve relevant knowledge "
            "rather than treating every question as an isolated interaction. "
            "Key areas explored: Context routing, knowledge retrieval, local language model integration, Llama-based workflows, "
            "and structured information processing. "
            "Building Vic-NLP significantly deepened my understanding of how AI systems maintain context and produce contextually relevant responses."
        ),
        "tags": ["vic-nlp", "nlp", "python", "llama", "context-routing", "retrieval", "local-llm"]
    },
    {
        "id": "proj-aurasync-01",
        "title": "AuraSync AI — AI-Powered Fashion Analysis",
        "category": "Projects",
        "project": "AuraSync AI",
        "content": (
            "AuraSync is an AI-powered fashion analysis web application. "
            "Tech stack: Next.js, TypeScript, Tailwind CSS, FastAPI, Supabase, and the Gemini API. "
            "The application provides AI-assisted fashion recommendations based on user-provided profile data and visual analysis. "
            "This project provided hands-on experience integrating AI capabilities into a complete, full-stack web application "
            "rather than treating the model as an isolated component."
        ),
        "tags": ["aurasync", "gemini-api", "nextjs", "fastapi", "supabase", "typescript", "fullstack"]
    },
    {
        "id": "proj-neurovoice-01",
        "title": "NeuroVoice AI — Voice-Based Health Risk Screening (Research Concept)",
        "category": "Projects",
        "project": "NeuroVoice AI",
        "content": (
            "NeuroVoice AI is a research concept project exploring voice-based Parkinson's disease risk screening using machine learning "
            "and quantum machine learning (QML) approaches. "
            "It investigated acoustic voice features, conventional machine learning classifiers, and quantum machine learning techniques using PennyLane/Qiskit. "
            "Crucially, it is an exploratory risk-screening research concept, NOT a medical diagnostic tool or clinical device. "
            "This project introduced me to the real-world complexities of applying ML to biometric data and healthcare-related datasets."
        ),
        "tags": ["neurovoice", "voice-analysis", "parkinsons", "qml", "machine-learning", "research-concept", "non-diagnostic"]
    },

    # --- Category: Technical Skills & Engineering ---
    {
        "id": "skills-01",
        "title": "Programming & Development Skills",
        "category": "Technical Skills",
        "project": None,
        "content": (
            "My practical programming stack includes: "
            "Languages: Python, TypeScript, JavaScript. "
            "Frontend: React, Next.js, Tailwind CSS, Framer Motion. "
            "Backend: FastAPI, Node.js, REST APIs, asynchronous programming. "
            "Engineering: Full frontend-to-backend architecture, database integration (PostgreSQL, Supabase), Git, GitHub open source workflows. "
            "My strongest practical foundation is in software development, particularly TypeScript, React, Python, and building end-to-end working applications."
        ),
        "tags": ["python", "typescript", "react", "nextjs", "fastapi", "nodejs", "software-engineering"]
    },
    {
        "id": "skills-02",
        "title": "AI, Generative AI & Quantum Stack",
        "category": "Technical Skills",
        "project": None,
        "content": (
            "My AI and quantum technology experience includes: "
            "Generative AI: LLM API integration (Gemini API, OpenAI), Llama-based local workflows, RAG architecture, "
            "context routing, conversational memory management, prompt engineering. "
            "Machine Learning: Classical ML models, feature extraction, evaluation metrics. "
            "Quantum Computing: Qiskit, PennyLane, quantum circuit design, state vector simulation, QASM, complex linear algebra."
        ),
        "tags": ["genai", "rag", "embeddings", "qiskit", "pennylane", "machine-learning"]
    },
    {
        "id": "proj-chatbot-01",
        "title": "AI Chatbot — Architecture & Tech Stack",
        "category": "Projects",
        "project": "AI Chatbot",
        "content": (
            "This AI Chatbot application itself is built as an interactive, context-aware voice agent and portfolio storytelling experience. "
            "Frontend: Built with Next.js 16 (App Router), TypeScript, Tailwind CSS v4, Lucide icons, Framer Motion, and native Web Speech API for voice recognition and synthesis. Hosted on Netlify. "
            "Backend: Built with Python and FastAPI, using Pydantic for validation, AsyncPG with pgvector (and in-memory cosine fallback) for RAG semantic search, and the Gemini API for grounded first-person reasoning. Hosted on Render Cloud. "
            "Architecture: Features live cosine similarity source attribution, chapter-aware conversational memory, audio visualization, and strict hallucination prevention."
        ),
        "tags": ["chatbot", "architecture", "fastapi", "nextjs", "tech-stack", "voice-agent", "rag"]
    },
    {
        "id": "genai-philosophy-01",
        "title": "Approach to Generative AI Engineering",
        "category": "Engineering Decisions",
        "project": None,
        "content": (
            "I believe moving beyond simple LLM API calls requires treating GenAI as a full systems engineering discipline. "
            "A reliable AI application requires: "
            "1. Retrieval-Augmented Generation (RAG) with semantic search and pgvector. "
            "2. Thoughtful context engineering and token budgeting. "
            "3. Robust conversational memory with coreference resolution. "
            "4. Guardrails and hallucination mitigation through source attribution and grounded prompts. "
            "5. Model evaluation and structured outputs. "
            "A useful AI application needs more than a powerful model; it requires reliable retrieval, thoughtful system architecture, "
            "evaluation, and accessible UX."
        ),
        "tags": ["genai-engineering", "rag-design", "context-engineering", "hallucination-prevention"]
    }
]

STORY_CHAPTERS: List[Dict[str, Any]] = [
    {
        "id": "chapter-1",
        "number": "01",
        "title": "The Beginning",
        "subtitle": "Curiosity, self-driven learning, and the spark of software engineering",
        "summary": "How curiosity led from a BSc in Information Technology to pursuing an MSc in Computer Science, discovering that software becomes alive when you understand how it works internally.",
        "narration": (
            "Every journey starts with a question. For me, that question was: 'How does this actually work underneath?' "
            "After completing my BSc in Information Technology, I chose to pursue an MSc in Computer Science to dig deeper into the core principles. "
            "I quickly realized I didn't want to just follow tutorials or copy existing templates; I wanted to build systems from the ground up."
        ),
        "key_themes": ["BSc IT to MSc Computer Science", "Internal Mechanics", "Curiosity-Driven Learning"],
        "projects_featured": [],
        "suggested_questions": [
            "What motivated you to pursue an MSc in Computer Science?",
            "How did you get started in software development?",
            "What does your day-to-day learning approach look like?"
        ],
        "quote": "I prefer understanding the underlying concept instead of blindly copying code."
    },
    {
        "id": "chapter-2",
        "number": "02",
        "title": "The Builder",
        "subtitle": "From learning frustrations to developer tools and complete applications",
        "summary": "Building QFoundry to visualize quantum circuits, authoring a zero-dependency TypeScript quantum engine, creating Vic-NLP, and shipping full-stack products like AuraSync.",
        "narration": (
            "I learn best by building. When I struggled to understand quantum circuits, I built QFoundry—a VS Code extension with Qiskit and React. "
            "Then, to truly master the underlying linear algebra and complex state vectors, I wrote QFoundry npm: an independent simulation engine in pure TypeScript. "
            "From there, I expanded into AI assistants with Vic-NLP and full-stack AI applications like AuraSync."
        ),
        "key_themes": ["QFoundry VS Code Tool", "QFoundry npm Zero-Dependency Engine", "Full-Stack Development"],
        "projects_featured": ["QFoundry", "QFoundry npm", "Vic-NLP", "AuraSync AI", "NeuroVoice AI"],
        "suggested_questions": [
            "Why did you build QFoundry, and what was the hardest challenge?",
            "How does your QFoundry npm simulator differ from Qiskit?",
            "What did you learn from building AuraSync AI?"
        ],
        "quote": "When I couldn't find a tool that explained quantum circuits visually, I built one myself."
    },
    {
        "id": "chapter-3",
        "number": "03",
        "title": "Exploring Intelligence",
        "subtitle": "Venturing into Generative AI, RAG architectures, and quantum ML",
        "summary": "Moving beyond API wrappers into context routing, vector embeddings, multi-layer memory, and exploring voice-based research in NeuroVoice AI.",
        "narration": (
            "Connecting an application to an LLM API is just the surface. Real AI engineering is about designing reliable systems: "
            "RAG pipelines with pgvector, context routing, conversational memory, and preventing hallucinations. "
            "With NeuroVoice AI, I explored voice features with ML and PennyLane quantum machine learning—always keeping it grounded as research, not medical claims."
        ),
        "key_themes": ["Generative AI Systems", "RAG & Vector Retrieval", "Quantum Machine Learning"],
        "projects_featured": ["Vic-NLP", "NeuroVoice AI", "AuraSync AI"],
        "suggested_questions": [
            "How do you approach building a production RAG pipeline?",
            "What was the research scope of NeuroVoice AI?",
            "How do you see the intersection between Quantum Computing and AI?"
        ],
        "quote": "A useful AI application needs more than a powerful model. It needs good context, reliable retrieval, and thoughtful architecture."
    },
    {
        "id": "chapter-4",
        "number": "04",
        "title": "The Thinking Process",
        "subtitle": "Navigating ambiguity, debugging failures, and building without a roadmap",
        "summary": "How I tackle unfamiliar technical domains: breaking problems down to fundamentals, making deliberate mistakes, and iterating until it works.",
        "narration": (
            "I don't need a complete roadmap before I begin. In fact, some of my best learning happened when I stepped into territory I knew little about, "
            "made mistakes, and figured out the missing pieces. "
            "When a system breaks, I don't apply quick patches; I look for why the failure happened in the first place."
        ),
        "key_themes": ["Problem Deconstruction", "Comfort with Ambiguity", "Persistence through Debugging"],
        "projects_featured": ["QFoundry npm", "Vic-NLP"],
        "suggested_questions": [
            "How do you approach a technology you have never worked with before?",
            "Can you tell me about a time an approach failed and how you resolved it?",
            "What are your biggest engineering strengths and where do you feel you need to grow?"
        ],
        "quote": "I am comfortable entering unfamiliar areas, learning what is necessary, and figuring things out."
    },
    {
        "id": "chapter-5",
        "number": "05",
        "title": "Beyond Today",
        "subtitle": "Career ambitions, areas of active growth, and the journey ahead",
        "summary": "Targeting a role as a Generative AI Engineer, deepening theoretical AI/ML foundations, and creating systems that solve real-world problems.",
        "narration": (
            "I am ready to bring my building mindset, adaptability, and curiosity to a high-impact engineering team. "
            "I am actively deepening my theoretical understanding of ML, refining production-grade GenAI architectures, and mastering system evaluation. "
            "My goal is simple: to build software that is useful, reliable, and pushes the boundary of what's possible."
        ),
        "key_themes": ["Generative AI Engineering", "Theoretical Growth", "Long-Term Impact"],
        "projects_featured": [],
        "suggested_questions": [
            "What kind of engineering role are you looking for right now?",
            "What specific areas of AI engineering are you focusing on mastering next?",
            "Where do you see yourself in the next few years?"
        ],
        "quote": "I am a builder driven by curiosity. I learn by understanding, experiment by building, and grow by taking on problems I haven't solved before."
    }
]

