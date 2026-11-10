"use client";

import React, { useState, useEffect, useRef } from "react";
import {
  Mic,
  MicOff,
  Send,
  Volume2,
  VolumeX,
  RotateCcw,
  X,
  Sparkles,
  ChevronDown,
  ChevronUp,
  ShieldCheck,
  Radio,
  BookOpen
} from "lucide-react";
import { ChatMessage, KnowledgeSource, ChatResponse } from "../types";
import { VoiceVisualizer } from "./VoiceVisualizer";

interface AIChatModalProps {
  isOpen: boolean;
  onClose: () => void;
  chapterContext?: string;
  initialQuery?: string;
  onClearInitialQuery?: () => void;
}

export const AIChatModal: React.FC<AIChatModalProps> = ({
  isOpen,
  onClose,
  chapterContext,
  initialQuery,
  onClearInitialQuery,
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome-msg",
      role: "assistant",
      content:
        "Hello! I am an AI representation of Victorraj. Ask me anything about my journey from BSc IT to MSc Computer Science, projects like QFoundry and Vic-NLP, my thinking process, or my ambitions in Generative AI engineering.",
      suggested_followups: [
        "Why did you build QFoundry?",
        "What is your approach to Generative AI engineering?",
        "How do you handle unfamiliar technical problems?"
      ],
      timestamp: "Intro",
    },
  ]);

  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [loadingSeconds, setLoadingSeconds] = useState(0);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voicePlaybackEnabled, setVoicePlaybackEnabled] = useState(true);
  const [expandedSourceId, setExpandedSourceId] = useState<string | null>(null);
  const [micError, setMicError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);
  const synthRef = useRef<SpeechSynthesis | null>(null);

  // Initialize Speech Synthesis and Speech Recognition
  useEffect(() => {
    if (typeof window !== "undefined") {
      synthRef.current = window.speechSynthesis;

      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.onstart = () => {
          setIsListening(true);
        };

        recognition.onresult = (event: any) => {
          const transcript = Array.from(event.results)
            .map((result: any) => result[0].transcript)
            .join("");
          setInput(transcript);
        };

        recognition.onerror = (event: any) => {
          setIsListening(false);
          if (event.error === "not-allowed" || event.error === "permission-denied") {
            setMicError("Microphone access denied. Please allow mic access in your browser settings and reload.");
          } else if (event.error === "no-speech") {
            setMicError(null); // silent, just stop
          } else {
            setMicError(`Voice error: ${event.error}`);
          }
        };

        recognition.onend = () => {
          setIsListening(false);
        };

        recognitionRef.current = recognition;
      }
    }

    return () => {
      if (synthRef.current) {
        synthRef.current.cancel();
      }
    };
  }, []);

  // Timer while loading to inform user if cloud server is waking up
  useEffect(() => {
    let interval: any;
    if (isLoading) {
      setLoadingSeconds(0);
      interval = setInterval(() => {
        setLoadingSeconds((prev) => prev + 1);
      }, 1000);
    } else {
      setLoadingSeconds(0);
    }
    return () => clearInterval(interval);
  }, [isLoading]);

  // Handle incoming initial queries (e.g. clicking suggested question from story)
  useEffect(() => {
    if (initialQuery && initialQuery.trim()) {
      handleSendMessage(initialQuery);
      if (onClearInitialQuery) onClearInitialQuery();
    }
  }, [initialQuery]);

  // Scroll to bottom
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isOpen, isLoading]);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      setMicError("Speech recognition is not supported in this browser. Please use Chrome or Edge.");
      return;
    }

    setMicError(null);
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      // Stop any current speaking before listening
      stopSpeaking();
      recognitionRef.current.start();
    }
  };

  const speakText = (text: string) => {
    if (!synthRef.current || !voicePlaybackEnabled) return;

    synthRef.current.cancel(); // Stop any ongoing speech
    
    // Clean text for speech (remove markdown symbols)
    const cleanSpeech = text
      .replace(/[*_#`\[\]]/g, "")
      .replace(/https?:\/\/\S+/g, "")
      .trim();

    const utterance = new SpeechSynthesisUtterance(cleanSpeech);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    // Pick a natural English voice if available
    const voices = synthRef.current.getVoices();
    const naturalVoice = voices.find(
      (v) =>
        v.lang.startsWith("en") &&
        (v.name.includes("Natural") ||
          v.name.includes("Daniel") ||
          v.name.includes("Google") ||
          v.name.includes("Samantha"))
    );
    if (naturalVoice) {
      utterance.voice = naturalVoice;
    }

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    synthRef.current.speak(utterance);
  };

  const stopSpeaking = () => {
    if (synthRef.current) {
      synthRef.current.cancel();
      setIsSpeaking(false);
    }
  };

  const handleSendMessage = async (textToSend?: string) => {
    const query = (textToSend || input).trim();
    if (!query || isLoading) return;

    setInput("");
    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop();
    }

    const userMessage: ChatMessage = {
      id: `usr-${Date.now()}`,
      role: "user",
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: query,
          session_id: "recruitment-session",
          chapter_context: chapterContext || "Story Overview",
        }),
      });

      if (!res.ok) {
        throw new Error(`Server returned ${res.status}`);
      }

      const data: ChatResponse = await res.json();

      const assistantMessage: ChatMessage = {
        id: `asst-${Date.now()}`,
        role: "assistant",
        content: data.response,
        sources: data.sources,
        suggested_followups: data.suggested_followups,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      if (voicePlaybackEnabled) {
        speakText(data.response);
      }
    } catch (err) {
      console.error("Chat error:", err);
      const errorMessage: ChatMessage = {
        id: `err-${Date.now()}`,
        role: "assistant",
        content:
          "I experienced an issue connecting to the AI backend service. Please verify that the FastAPI backend server is running on port 8000.",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearHistory = async () => {
    stopSpeaking();
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      await fetch(`${apiUrl}/api/chat/clear`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: "recruitment-session" }),
      });
    } catch (e) {
      // ignore
    }
    setMessages([
      {
        id: "fresh-msg",
        role: "assistant",
        content: "Conversation history cleared. What would you like to explore next?",
        suggested_followups: [
          "Tell me about QFoundry npm.",
          "What is your approach to RAG architectures?",
          "Where do you see yourself growing in AI?"
        ],
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      },
    ]);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="bg-[#0f1115] border border-white/[0.1] rounded-2xl w-full max-w-4xl h-[90vh] max-h-[820px] flex flex-col shadow-2xl overflow-hidden">
        
        {/* Header Bar */}
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-white/[0.08] bg-[#121418]">
          <div className="flex items-center gap-3">
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
            <div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-semibold text-[#f5f5f2] tracking-wide">
                  AI Chatbot
                </span>
                <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-white/[0.06] text-neutral-400">
                  Voice & RAG Grounded
                </span>
              </div>
              <p className="text-[11px] text-neutral-400">
                Context: {chapterContext || "General Conversation"}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {/* Speaking / Audio Status Indicator */}
            {isSpeaking && (
              <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-white/[0.06] text-neutral-300 text-xs">
                <VoiceVisualizer isActive={true} color="bg-emerald-400" />
                <span className="text-[11px] font-mono">Speaking</span>
                <button
                  onClick={stopSpeaking}
                  className="ml-1 text-[10px] text-neutral-400 hover:text-white underline"
                >
                  Stop
                </button>
              </div>
            )}

            {/* Voice playback toggle */}
            <button
              onClick={() => {
                if (isSpeaking) stopSpeaking();
                setVoicePlaybackEnabled(!voicePlaybackEnabled);
              }}
              className={`p-2 rounded-lg border text-xs transition-colors flex items-center gap-1 ${
                voicePlaybackEnabled
                  ? "border-white/10 text-neutral-200 bg-white/[0.04] hover:bg-white/[0.08]"
                  : "border-transparent text-neutral-500 hover:text-neutral-300"
              }`}
              title={voicePlaybackEnabled ? "Voice output enabled (click to mute)" : "Voice output muted (click to unmute)"}
            >
              {voicePlaybackEnabled ? <Volume2 size={16} /> : <VolumeX size={16} />}
            </button>

            {/* Clear conversation */}
            <button
              onClick={handleClearHistory}
              className="p-2 rounded-lg border border-transparent text-neutral-400 hover:text-neutral-200 hover:bg-white/[0.05] transition-colors"
              title="Reset conversation"
            >
              <RotateCcw size={16} />
            </button>

            {/* Close modal */}
            <button
              onClick={() => {
                stopSpeaking();
                if (isListening && recognitionRef.current) recognitionRef.current.stop();
                onClose();
              }}
              className="p-2 rounded-lg border border-transparent text-neutral-400 hover:text-white hover:bg-white/[0.05] transition-colors"
              title="Close chat"
            >
              <X size={18} />
            </button>
          </div>
        </div>

        {/* Message History Container */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}
            >
              <div className="flex items-center gap-2 mb-1.5 px-1">
                <span className="text-[11px] font-mono text-neutral-400">
                  {msg.role === "user" ? "Interviewer" : "Victorraj (AI Representation)"}
                </span>
                <span className="text-[10px] text-neutral-600 font-mono">
                  {msg.timestamp}
                </span>
              </div>

              <div
                className={`max-w-[90%] sm:max-w-[82%] rounded-2xl p-4 text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-[#1f232b] text-[#f5f5f2] border border-white/[0.08] rounded-tr-sm"
                    : "bg-[#14161b] text-[#e8e8e4] border border-white/[0.06] rounded-tl-sm shadow-sm"
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>

                {/* Voice play button for assistant message */}
                {msg.role === "assistant" && (
                  <div className="mt-3 pt-2.5 border-t border-white/[0.05] flex items-center justify-between text-xs text-neutral-400">
                    <button
                      onClick={() => speakText(msg.content)}
                      className="hover:text-white transition-colors flex items-center gap-1.5 text-[11px]"
                    >
                      <Volume2 size={13} />
                      <span>Listen to voice</span>
                    </button>

                    {/* Sources badge if available */}
                    {msg.sources && msg.sources.length > 0 && (
                      <button
                        onClick={() =>
                          setExpandedSourceId(
                            expandedSourceId === msg.id ? null : msg.id
                          )
                        }
                        className="hover:text-white transition-colors flex items-center gap-1 text-[11px] text-neutral-400"
                      >
                        <ShieldCheck size={13} className="text-emerald-400/80" />
                        <span>{msg.sources.length} Grounded Citations</span>
                        {expandedSourceId === msg.id ? (
                          <ChevronUp size={12} />
                        ) : (
                          <ChevronDown size={12} />
                        )}
                      </button>
                    )}
                  </div>
                )}

                {/* Grounding Citations Dropdown */}
                {expandedSourceId === msg.id && msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3 p-3 rounded-lg bg-black/40 border border-white/[0.06] space-y-2.5">
                    <div className="flex items-center justify-between text-[11px] font-mono text-neutral-400 border-b border-white/[0.04] pb-1">
                      <span>RAG KNOWLEDGE RETRIEVAL AUDIT</span>
                      <span>Cosine Similarity</span>
                    </div>
                    {msg.sources.map((src) => (
                      <div key={src.id} className="text-xs space-y-1">
                        <div className="flex items-center justify-between text-neutral-300 font-medium">
                          <span className="truncate">{src.title}</span>
                          <span className="font-mono text-[10px] text-emerald-400/90 ml-2">
                            {(src.similarity_score * 100).toFixed(1)}% match
                          </span>
                        </div>
                        <p className="text-[11px] text-neutral-400 italic line-clamp-2">
                          "{src.snippet}"
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

                {/* Suggested follow-ups */}
                {msg.suggested_followups && msg.suggested_followups.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-2 max-w-[85%]">
                    {msg.suggested_followups.map((followup, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSendMessage(followup)}
                        className="text-[11px] px-3 py-1.5 rounded-full bg-white/[0.04] hover:bg-white/[0.08] text-neutral-300 hover:text-white border border-white/[0.05] transition-all flex items-center gap-1.5 text-left"
                      >
                        <Sparkles size={11} className="text-neutral-400" />
                        <span>{followup}</span>
                      </button>
                    ))}
                  </div>
                )}
            </div>
          ))}

          {/* Thinking / retrieving indicator */}
          {isLoading && (
            <div className="flex flex-col items-start space-y-2">
              <div className="flex items-center gap-2 mb-1 px-1">
                <span className="text-[11px] font-mono text-neutral-400">
                  Victorraj (AI Representation)
                </span>
              </div>
              <div className="bg-[#14161b] border border-white/[0.06] rounded-2xl rounded-tl-sm p-4 flex flex-col gap-1.5">
                <div className="flex items-center gap-3">
                  <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                  <span className="text-xs text-neutral-300 font-mono">
                    {loadingSeconds >= 5
                      ? `Waking up cloud server from standby (${loadingSeconds}s)...`
                      : "Retrieving knowledge chunks & evaluating response..."}
                  </span>
                </div>
                {loadingSeconds >= 5 && (
                  <span className="text-[11px] text-neutral-500 pl-7">
                    Free-tier cloud servers sleep during inactivity. First request takes ~30s to boot up. Subsequent replies will be instant!
                  </span>
                )}
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="p-4 border-t border-white/[0.08] bg-[#121418]">
          {/* Mic permission error banner */}
          {micError && (
            <div className="flex items-center justify-between mb-3 px-3 py-2 rounded-lg bg-red-500/10 border border-red-500/20 text-red-300 text-xs">
              <div className="flex items-center gap-2">
                <MicOff size={13} />
                <span>{micError}</span>
              </div>
              <button onClick={() => setMicError(null)} className="ml-2 text-red-400 hover:text-red-200">
                <X size={13} />
              </button>
            </div>
          )}

          {/* Live listening banner */}
          {isListening && (
            <div className="flex items-center justify-between mb-3 px-3 py-2 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs">
              <div className="flex items-center gap-2">
                <Radio size={14} className="animate-pulse" />
                <span>Listening... Speak your question into your microphone</span>
              </div>
              <VoiceVisualizer isActive={true} color="bg-emerald-400" />
            </div>
          )}

          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center gap-2"
          >
            {/* Microphone Button */}
            <button
              type="button"
              onClick={toggleListening}
              className={`p-3 rounded-xl border transition-all ${
                isListening
                  ? "bg-red-500/20 border-red-500/40 text-red-300 animate-pulse"
                  : "bg-white/[0.04] border-white/[0.08] text-neutral-300 hover:text-white hover:bg-white/[0.08]"
              }`}
              title={isListening ? "Stop listening" : "Ask with microphone"}
            >
              {isListening ? <MicOff size={18} /> : <Mic size={18} />}
            </button>

            {/* Text Input */}
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about Victorraj's background, projects, or thinking..."
              disabled={isLoading}
              className="flex-1 bg-black/40 border border-white/[0.08] focus:border-white/[0.2] rounded-xl px-4 py-3 text-sm text-[#f5f5f2] placeholder:text-neutral-500 outline-none transition-colors"
            />

            {/* Send Button */}
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="p-3 rounded-xl bg-white/[0.08] hover:bg-white/[0.15] disabled:opacity-30 disabled:cursor-not-allowed border border-white/[0.08] text-white transition-colors"
              title="Send message"
            >
              <Send size={18} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
