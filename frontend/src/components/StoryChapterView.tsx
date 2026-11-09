"use client";

import React, { useState, useEffect, useRef } from "react";
import { StoryChapter } from "../types";
import { ProjectCard } from "./ProjectCard";
import { Volume2, VolumeX, Sparkles, ArrowRight, Quote } from "lucide-react";
import { VoiceVisualizer } from "./VoiceVisualizer";

interface StoryChapterViewProps {
  chapter: StoryChapter;
  onAskQuestion: (question: string) => void;
  onNextChapter?: () => void;
  isLastChapter?: boolean;
}

export const StoryChapterView: React.FC<StoryChapterViewProps> = ({
  chapter,
  onAskQuestion,
  onNextChapter,
  isLastChapter = false,
}) => {
  const [isPlayingNarration, setIsPlayingNarration] = useState(false);
  const synthRef = useRef<SpeechSynthesis | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      synthRef.current = window.speechSynthesis;
    }
    return () => {
      if (synthRef.current) {
        synthRef.current.cancel();
      }
    };
  }, [chapter.id]);

  const toggleNarration = () => {
    if (!synthRef.current) return;

    if (isPlayingNarration) {
      synthRef.current.cancel();
      setIsPlayingNarration(false);
    } else {
      synthRef.current.cancel();
      const utterance = new SpeechSynthesisUtterance(chapter.narration);
      utterance.rate = 0.95;
      utterance.pitch = 1.0;

      const voices = synthRef.current.getVoices();
      const naturalVoice = voices.find(
        (v) =>
          v.lang.startsWith("en") &&
          (v.name.includes("Natural") ||
            v.name.includes("Daniel") ||
            v.name.includes("Google") ||
            v.name.includes("Samantha"))
      );
      if (naturalVoice) utterance.voice = naturalVoice;

      utterance.onstart = () => setIsPlayingNarration(true);
      utterance.onend = () => setIsPlayingNarration(false);
      utterance.onerror = () => setIsPlayingNarration(false);

      synthRef.current.speak(utterance);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-10 animate-in fade-in duration-300">
      {/* Chapter Header */}
      <div className="space-y-4">
        <div className="flex items-center justify-between border-b border-white/[0.08] pb-4">
          <div className="flex items-center gap-3">
            <span className="font-mono text-xs uppercase tracking-widest text-neutral-400">
              Chapter {chapter.number}
            </span>
            <span className="text-white/20">•</span>
            <span className="text-xs text-neutral-500 font-mono">Story Mode</span>
          </div>

          {/* Narration Listen Button */}
          <button
            onClick={toggleNarration}
            className={`flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs transition-colors ${
              isPlayingNarration
                ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-300"
                : "bg-white/[0.03] border-white/[0.08] text-neutral-300 hover:text-white hover:bg-white/[0.06]"
            }`}
          >
            {isPlayingNarration ? (
              <>
                <VoiceVisualizer isActive={true} color="bg-emerald-400" />
                <span>Pause Narration</span>
              </>
            ) : (
              <>
                <Volume2 size={13} />
                <span>Listen to Narration</span>
              </>
            )}
          </button>
        </div>

        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-light tracking-tight text-[#f5f5f2] font-serif">
          {chapter.title}
        </h1>

        <p className="text-base sm:text-lg text-neutral-400 font-normal leading-relaxed max-w-2xl">
          {chapter.subtitle}
        </p>

        {/* Key Themes */}
        <div className="flex flex-wrap gap-2 pt-2">
          {chapter.key_themes.map((theme, i) => (
            <span
              key={i}
              className="text-xs px-2.5 py-1 rounded-md bg-white/[0.04] text-neutral-300 border border-white/[0.06] font-mono"
            >
              #{theme}
            </span>
          ))}
        </div>
      </div>

      {/* Main Narrative Excerpt */}
      <div className="prose prose-invert max-w-none">
        <div className="bg-[#121418] border border-white/[0.06] rounded-2xl p-6 sm:p-8 relative">
          <p className="text-base sm:text-lg text-neutral-200 leading-relaxed font-light">
            {chapter.narration}
          </p>

          {chapter.quote && (
            <div className="mt-6 pt-6 border-t border-white/[0.06] flex items-start gap-3">
              <Quote size={20} className="text-neutral-500 shrink-0 mt-0.5" />
              <p className="text-sm italic text-neutral-400 font-serif">
                "{chapter.quote}"
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Featured Projects (if any in this chapter) */}
      {chapter.projects_featured.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-mono uppercase tracking-wider text-neutral-400">
              Featured Projects in this Chapter
            </h2>
            <span className="text-xs text-neutral-500">Click to explore code or ask AI</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {chapter.projects_featured.map((proj) => (
              <ProjectCard
                key={proj}
                projectName={proj}
                onAskAboutProject={(name) => onAskQuestion(`Tell me about ${name} and the engineering decisions behind it.`)}
              />
            ))}
          </div>
        </div>
      )}

      {/* Suggested Questions for Interviewer */}
      <div className="bg-[#101216] border border-white/[0.06] rounded-2xl p-6 space-y-4">
        <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-neutral-400">
          <Sparkles size={14} className="text-neutral-400" />
          <span>Suggested Questions to Ask Victorraj (AI)</span>
        </div>
        <p className="text-xs text-neutral-500">
          Click any question below to immediately ask the conversational voice agent with grounded context:
        </p>

        <div className="space-y-2">
          {chapter.suggested_questions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => onAskQuestion(q)}
              className="w-full text-left p-3 rounded-xl bg-white/[0.03] hover:bg-white/[0.07] border border-white/[0.04] hover:border-white/[0.1] text-sm text-neutral-300 hover:text-white transition-all flex items-center justify-between group"
            >
              <span>{q}</span>
              <ArrowRight
                size={14}
                className="text-neutral-500 group-hover:text-white group-hover:translate-x-0.5 transition-all"
              />
            </button>
          ))}
        </div>
      </div>

      {/* Navigation Controls */}
      <div className="pt-6 border-t border-white/[0.08] flex items-center justify-between">
        <span className="text-xs font-mono text-neutral-500">
          {chapter.number} of 05
        </span>

        {onNextChapter && !isLastChapter && (
          <button
            onClick={onNextChapter}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/[0.08] hover:bg-white/[0.14] text-white text-sm font-medium transition-colors"
          >
            <span>Proceed to Next Chapter</span>
            <ArrowRight size={15} />
          </button>
        )}
      </div>
    </div>
  );
};

