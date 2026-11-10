"use client";

import React, { useState, useEffect } from "react";
import {
  Mic,
  ArrowRight,
  BookOpen,
  MessageSquare,
  Sparkles,
  Volume2,
  ChevronRight,
  Code2,
  Brain,
  Compass,
  Rocket
} from "lucide-react";
import { StoryChapter } from "../types";
import { StoryChapterView } from "../components/StoryChapterView";
import { AIChatModal } from "../components/AIChatModal";
import { VoiceVisualizer } from "../components/VoiceVisualizer";

// Fallback chapters if backend is loading
const FALLBACK_CHAPTERS: StoryChapter[] = [
  {
    id: "chapter-1",
    number: "01",
    title: "The Beginning",
    subtitle: "Curiosity, self-driven learning, and the spark of software engineering",
    summary: "How curiosity led from a BSc in Information Technology to pursuing an MSc in Computer Science, discovering that software becomes alive when you understand how it works internally.",
    narration: "Every journey starts with a question. For me, that question was: 'How does this actually work underneath?' After completing my BSc in Information Technology, I chose to pursue an MSc in Computer Science to dig deeper into the core principles. I quickly realized I didn't want to just follow tutorials or copy existing templates; I wanted to build systems from the ground up.",
    key_themes: ["BSc IT to MSc Computer Science", "Internal Mechanics", "Curiosity-Driven Learning"],
    projects_featured: [],
    suggested_questions: [
      "What motivated you to pursue an MSc in Computer Science?",
      "How did you get started in software development?",
      "What does your day-to-day learning approach look like?"
    ],
    quote: "I prefer understanding the underlying concept instead of blindly copying code."
  },
  {
    id: "chapter-2",
    number: "02",
    title: "The Builder",
    subtitle: "From learning frustrations to developer tools and complete applications",
    summary: "Building QFoundry to visualize quantum circuits, authoring a zero-dependency TypeScript quantum engine, creating Vic-NLP, and shipping full-stack products like AuraSync.",
    narration: "I learn best by building. When I struggled to understand quantum circuits, I built QFoundry—a VS Code extension with Qiskit and React. Then, to truly master the underlying linear algebra and complex state vectors, I wrote QFoundry npm: an independent simulation engine in pure TypeScript without any external dependencies. From there, I expanded into AI assistants with Vic-NLP and full-stack AI applications like AuraSync.",
    key_themes: ["QFoundry VS Code Tool", "QFoundry npm Zero-Dependency Engine", "Full-Stack Development"],
    projects_featured: ["QFoundry", "QFoundry npm", "Vic-NLP", "AuraSync AI", "NeuroVoice AI"],
    suggested_questions: [
      "Why did you build QFoundry, and what was the hardest challenge?",
      "How does your QFoundry npm simulator differ from Qiskit?",
      "What did you learn from building AuraSync AI?"
    ],
    quote: "When I couldn't find a tool that explained quantum circuits visually, I built one myself."
  },
  {
    id: "chapter-3",
    number: "03",
    title: "Exploring Intelligence",
    subtitle: "Venturing into Generative AI, RAG architectures, and quantum ML",
    summary: "Moving beyond API wrappers into context routing, vector embeddings, multi-layer memory, and exploring voice-based research in NeuroVoice AI.",
    narration: "Connecting an application to an LLM API is just the surface. Real AI engineering is about designing reliable systems: RAG pipelines with pgvector, context routing, conversational memory, and preventing hallucinations. With NeuroVoice AI, I explored voice features with ML and PennyLane quantum machine learning—always keeping it grounded as research, not medical claims.",
    key_themes: ["Generative AI Systems", "RAG & Vector Retrieval", "Quantum Machine Learning"],
    projects_featured: ["Vic-NLP", "NeuroVoice AI", "AuraSync AI"],
    suggested_questions: [
      "How do you approach building a production RAG pipeline?",
      "What was the research scope of NeuroVoice AI?",
      "How do you see the intersection between Quantum Computing and AI?"
    ],
    quote: "A useful AI application needs more than a powerful model. It needs good context, reliable retrieval, and thoughtful architecture."
  },
  {
    id: "chapter-4",
    number: "04",
    title: "The Thinking Process",
    subtitle: "Navigating ambiguity, debugging failures, and building without a roadmap",
    summary: "How I tackle unfamiliar technical domains: breaking problems down to fundamentals, making deliberate mistakes, and iterating until it works.",
    narration: "I don't need a complete roadmap before I begin. In fact, some of my best learning happened when I stepped into territory I knew little about, made mistakes, and figured out the missing pieces. When a system breaks, I don't apply quick patches; I look for why the failure happened in the first place.",
    key_themes: ["Problem Deconstruction", "Comfort with Ambiguity", "Persistence through Debugging"],
    projects_featured: ["QFoundry npm", "Vic-NLP"],
    suggested_questions: [
      "How do you approach a technology you have never worked with before?",
      "Can you tell me about a time an approach failed and how you resolved it?",
      "What are your biggest engineering strengths and where do you feel you need to grow?"
    ],
    quote: "I am comfortable entering unfamiliar areas, learning what is necessary, and figuring things out."
  },
  {
    id: "chapter-5",
    number: "05",
    title: "Beyond Today",
    subtitle: "Career ambitions, areas of active growth, and the journey ahead",
    summary: "Targeting a role as a Generative AI Engineer, deepening theoretical AI/ML foundations, and creating systems that solve real-world problems.",
    narration: "I am ready to bring my building mindset, adaptability, and curiosity to a high-impact engineering team. I am actively deepening my theoretical understanding of ML, refining production-grade GenAI architectures, and mastering system evaluation. My goal is simple: to build software that is useful, reliable, and pushes the boundary of what's possible.",
    key_themes: ["Generative AI Engineering", "Theoretical Growth", "Long-Term Impact"],
    projects_featured: [],
    suggested_questions: [
      "What kind of engineering role are you looking for right now?",
      "What specific areas of AI engineering are you focusing on mastering next?",
      "Where do you see yourself in the next few years?"
    ],
    quote: "I am a builder driven by curiosity. I learn by understanding, experiment by building, and grow by taking on problems I haven't solved before."
  }
];

export default function Home() {
  const [hasStartedStory, setHasStartedStory] = useState(false);
  const [currentChapterIndex, setCurrentChapterIndex] = useState(0);
  const [chapters, setChapters] = useState<StoryChapter[]>(FALLBACK_CHAPTERS);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [pendingQuery, setPendingQuery] = useState<string | null>(null);

  // Fetch chapters from backend if available
  useEffect(() => {
    const fetchChapters = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${apiUrl}/api/story/chapters`);
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data) && data.length > 0) {
            setChapters(data);
          }
        }
      } catch (e) {
        // Fallback used automatically
      }
    };
    fetchChapters();
  }, []);

  const currentChapter = chapters[currentChapterIndex] || FALLBACK_CHAPTERS[0];

  const handleAskQuestion = (question: string) => {
    setPendingQuery(question);
    setIsChatOpen(true);
  };

  const handleNextChapter = () => {
    if (currentChapterIndex < chapters.length - 1) {
      setCurrentChapterIndex(currentChapterIndex + 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#0b0c0e] text-[#f5f5f2] relative selection:bg-neutral-800 selection:text-white">
      {/* Background Subtle Gradient & Grid lines */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-white/[0.015] blur-3xl rounded-full" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.015)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]" />
      </div>

      {/* Top Header */}
      <header className="sticky top-0 z-40 w-full border-b border-white/[0.06] bg-[#0b0c0e]/85 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                setHasStartedStory(false);
                setCurrentChapterIndex(0);
              }}
              className="flex items-center gap-2 group text-left"
            >
              <div className="w-6 h-6 rounded-md bg-white/[0.08] border border-white/[0.1] flex items-center justify-center font-mono text-xs text-neutral-300 group-hover:border-white/30 transition-colors">
                AI
              </div>
              <span className="text-sm font-medium tracking-wide text-[#f5f5f2] group-hover:text-white">
                AI Chatbot
              </span>
            </button>
            <span className="text-white/20 hidden sm:inline">•</span>
            <span className="text-xs text-neutral-500 font-mono hidden sm:inline">
              Candidate Representation
            </span>
          </div>

          {/* Quick Voice / Chat Trigger */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsChatOpen(true)}
              className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/[0.05] hover:bg-white/[0.1] border border-white/[0.08] text-neutral-200 text-xs font-medium transition-all group shadow-sm"
            >
              <Mic size={14} className="text-emerald-400 group-hover:scale-110 transition-transform" />
              <span>Ask AI / Voice Chat</span>
            </button>
          </div>
        </div>

        {/* Story Reading Progress Bar (when story mode active) */}
        {hasStartedStory && (
          <div className="w-full bg-white/[0.04] h-[2px]">
            <div
              className="bg-white/40 h-[2px] transition-all duration-300"
              style={{
                width: `${((currentChapterIndex + 1) / chapters.length) * 100}%`,
              }}
            />
          </div>
        )}
      </header>

      {/* Main Content Area */}
      <main className="flex-1 relative z-10">
        {!hasStartedStory ? (
          /* ============================================================ */
          /* OPENING HERO SCREEN                                           */
          /* ============================================================ */
          <div className="min-h-[calc(100vh-4rem)] flex flex-col justify-center items-center px-4 sm:px-6 py-20 text-center max-w-4xl mx-auto">
            {/* Subtle Voice Interaction Indicator */}
            <div className="mb-8 inline-flex items-center gap-2.5 px-3.5 py-1.5 rounded-full bg-white/[0.03] border border-white/[0.08] text-xs text-neutral-400 font-mono">
              <VoiceVisualizer isActive={true} color="bg-neutral-400" />
              <span>Context-Aware Voice Agent Ready</span>
            </div>

            {/* Main Headline */}
            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-light tracking-tight text-[#f5f5f2] mb-6 font-serif max-w-3xl leading-[1.15]">
              Every journey starts with a question.
            </h1>

            {/* Supporting Text */}
            <p className="text-lg sm:text-xl text-neutral-400 max-w-xl font-light leading-relaxed mb-12">
              Explore the experiences, ideas, projects and thinking behind the person.
            </p>

            {/* Interactive Primary Button */}
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <button
                onClick={() => setHasStartedStory(true)}
                className="flex items-center gap-3 px-8 py-4 rounded-full bg-[#f5f5f2] hover:bg-white text-black font-medium text-sm tracking-wide transition-all shadow-lg hover:scale-[1.02] active:scale-[0.98]"
              >
                <span>Begin the experience</span>
                <ArrowRight size={16} />
              </button>

              <button
                onClick={() => setIsChatOpen(true)}
                className="flex items-center gap-2.5 px-6 py-4 rounded-full bg-white/[0.04] hover:bg-white/[0.08] text-neutral-300 hover:text-white border border-white/[0.08] text-sm font-medium transition-all"
              >
                <Mic size={15} className="text-emerald-400" />
                <span>Ask via Voice or Text directly</span>
              </button>
            </div>

            {/* Quick Overview Badges */}
            <div className="mt-20 pt-10 border-t border-white/[0.06] grid grid-cols-2 sm:grid-cols-3 gap-6 text-left max-w-2xl w-full">
              <div>
                <span className="text-[11px] font-mono text-neutral-500 uppercase block mb-1">
                  Candidate
                </span>
                <span className="text-sm text-neutral-300 font-medium">Victorraj</span>
              </div>
              <div>
                <span className="text-[11px] font-mono text-neutral-500 uppercase block mb-1">
                  Education
                </span>
                <span className="text-sm text-neutral-300 font-medium">MSc Comp Sci (BSc IT)</span>
              </div>
              <div>
                <span className="text-[11px] font-mono text-neutral-500 uppercase block mb-1">
                  Core Projects
                </span>
                <span className="text-sm text-neutral-300 font-medium">QFoundry, Vic-NLP</span>
              </div>

            </div>
          </div>
        ) : (
          /* ============================================================ */
          /* INTERACTIVE STORY MODE (CHAPTERS)                           */
          /* ============================================================ */
          <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10">
            {/* Chapter Navigation Tabs */}
            <div className="mb-12 overflow-x-auto pb-2 scrollbar-none">
              <div className="flex items-center gap-2 min-w-max border-b border-white/[0.06] pb-3">
                {chapters.map((chap, idx) => {
                  const isActive = idx === currentChapterIndex;
                  return (
                    <button
                      key={chap.id}
                      onClick={() => {
                        setCurrentChapterIndex(idx);
                        window.scrollTo({ top: 0, behavior: "smooth" });
                      }}
                      className={`px-4 py-2 rounded-xl text-xs font-mono transition-all flex items-center gap-2 ${
                        isActive
                          ? "bg-white/[0.1] text-white border border-white/[0.15] shadow-sm"
                          : "text-neutral-500 hover:text-neutral-300 hover:bg-white/[0.03]"
                      }`}
                    >
                      <span className="opacity-60">{chap.number}</span>
                      <span>{chap.title}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Current Chapter View */}
            <StoryChapterView
              chapter={currentChapter}
              onAskQuestion={handleAskQuestion}
              onNextChapter={handleNextChapter}
              isLastChapter={currentChapterIndex === chapters.length - 1}
            />
          </div>
        )}
      </main>

      {/* Floating Bottom Quick Voice/Chat Drawer Trigger */}
      {hasStartedStory && (
        <div className="fixed bottom-20 right-6 z-40 animate-in fade-in slide-in-from-bottom-4 duration-300">
          <button
            onClick={() => setIsChatOpen(true)}
            className="flex items-center gap-3 px-5 py-3 rounded-full bg-[#181a20] hover:bg-[#20232a] text-[#f5f5f2] border border-white/[0.15] shadow-2xl transition-all hover:scale-105 active:scale-95 group"
          >
            <div className="w-8 h-8 rounded-full bg-white/[0.08] flex items-center justify-center text-emerald-400 group-hover:bg-white/[0.12] transition-colors">
              <Mic size={16} />
            </div>
            <div className="text-left pr-2">
              <span className="block text-xs font-medium">Ask Victorraj (AI)</span>
              <span className="block text-[10px] text-neutral-400 font-mono">Microphone or Text</span>
            </div>
          </button>
        </div>
      )}

      {/* Conversational AI Voice & Text Modal */}
      <AIChatModal
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        chapterContext={
          hasStartedStory
            ? `Chapter ${currentChapter.number}: ${currentChapter.title}`
            : "Opening Journey"
        }
        initialQuery={pendingQuery || undefined}
        onClearInitialQuery={() => setPendingQuery(null)}
      />
    </div>
  );
}
