"use client";

import React from "react";
import { ExternalLink, Package, Terminal, Cpu, Sparkles, Code2 } from "lucide-react";

interface ProjectDetails {
  name: string;
  category: string;
  tagline: string;
  description: string;
  stack: string[];
  github?: string;
  website?: string;
  npm?: string;
  badge?: string;
}

const PROJECTS_DATA: Record<string, ProjectDetails> = {
  "QFoundry": {
    name: "QFoundry",
    category: "Developer Tool / Extension",
    tagline: "Quantum Circuit Visualizer & Local Simulator for VS Code",
    description: "Built to bridge the gap between quantum theory and implementation. Provides gate-by-gate execution timelines, state-vector analysis, phase visualization, and QASM visualization.",
    stack: ["TypeScript", "React", "Python", "Qiskit", "VS Code API"],
    github: "https://github.com/Victorraj020/QFoundry",
    website: "https://qfoundry.netlify.app/",
    badge: "Open Source"
  },
  "QFoundry npm": {
    name: "QFoundry npm",
    category: "Simulation Engine",
    tagline: "Zero-Dependency Quantum Simulator in Pure TypeScript",
    description: "An independent quantum circuit simulation engine built from mathematical first principles. Implements complex number arithmetic, matrix operations, and state-vector simulation for up to 16 qubits without Python or runtime dependencies.",
    stack: ["TypeScript", "Linear Algebra", "Complex Numbers", "npm Package"],
    npm: "https://www.npmjs.com/package/qfoundry",
    badge: "Published npm"
  },
  "Vic-NLP": {
    name: "Vic-NLP",
    category: "Contextual AI Assistant",
    tagline: "Layered Context Routing & Local Knowledge Retrieval",
    description: "Explored structured context processing layers to maintain conversational coherence instead of treating questions in isolation. Leveraged local Llama workflows.",
    stack: ["Python", "Local LLM", "Llama", "Context Routing", "RAG"],
    badge: "AI Research"
  },
  "AuraSync AI": {
    name: "AuraSync AI",
    category: "Full-Stack AI Application",
    tagline: "Multimodal AI-Powered Fashion Recommendations",
    description: "An end-to-end full-stack application delivering personalized fashion analysis. Integrates Gemini API with reactive frontend state and secure backend database workflows.",
    stack: ["Next.js", "TypeScript", "Tailwind CSS", "FastAPI", "Supabase", "Gemini API"],
    badge: "Full-Stack AI"
  },
  "NeuroVoice AI": {
    name: "NeuroVoice AI",
    category: "Health Risk-Screening Research Concept",
    tagline: "Acoustic Biomarkers & Quantum Machine Learning",
    description: "Exploratory research concept investigating voice feature extraction, classical ML classifiers, and PennyLane/Qiskit quantum ML for Parkinson's risk indicators. Strictly an exploratory research concept, non-diagnostic.",
    stack: ["Python", "PennyLane", "Qiskit", "Machine Learning", "Acoustics"],
    badge: "Research Concept"
  }
};

interface ProjectCardProps {
  projectName: string;
  onAskAboutProject?: (projectName: string) => void;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({ projectName, onAskAboutProject }) => {
  const project = PROJECTS_DATA[projectName];
  if (!project) return null;

  return (
    <div className="bg-[#121418] border border-white/[0.08] rounded-xl p-5 hover:border-white/[0.18] transition-all duration-200 group flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between gap-2 mb-2">
          <span className="text-xs uppercase tracking-wider text-neutral-400 font-mono">
            {project.category}
          </span>
          {project.badge && (
            <span className="text-[11px] px-2 py-0.5 rounded-full bg-white/[0.06] text-neutral-300 font-mono border border-white/[0.06]">
              {project.badge}
            </span>
          )}
        </div>

        <h3 className="text-lg font-medium text-[#f5f5f2] mb-1 group-hover:text-white transition-colors">
          {project.name}
        </h3>
        
        <p className="text-xs text-neutral-400 font-normal mb-3 italic">
          {project.tagline}
        </p>

        <p className="text-xs text-neutral-300 leading-relaxed mb-4">
          {project.description}
        </p>
      </div>

      <div>
        <div className="flex flex-wrap gap-1.5 mb-4">
          {project.stack.map((tech) => (
            <span
              key={tech}
              className="text-[10px] px-2 py-0.5 rounded bg-black/40 text-neutral-300 border border-white/[0.04] font-mono"
            >
              {tech}
            </span>
          ))}
        </div>

        <div className="flex items-center justify-between pt-3 border-t border-white/[0.05]">
          <div className="flex items-center gap-3">
            {project.github && (
              <a
                href={project.github}
                target="_blank"
                rel="noreferrer"
                className="text-neutral-400 hover:text-white transition-colors inline-flex items-center gap-1 text-xs"
                title="View GitHub Repository"
              >
                <Code2 size={14} />
                <span className="underline-offset-2 hover:underline">Code</span>
              </a>
            )}
            {project.website && (
              <a
                href={project.website}
                target="_blank"
                rel="noreferrer"
                className="text-neutral-400 hover:text-white transition-colors inline-flex items-center gap-1 text-xs"
                title="Open Live Website"
              >
                <ExternalLink size={14} />
                <span className="underline-offset-2 hover:underline">Live Demo</span>
              </a>
            )}
            {project.npm && (
              <a
                href={project.npm}
                target="_blank"
                rel="noreferrer"
                className="text-neutral-400 hover:text-white transition-colors inline-flex items-center gap-1 text-xs"
                title="View npm Package"
              >
                <Package size={14} />
                <span className="underline-offset-2 hover:underline">npm</span>
              </a>
            )}
          </div>

          {onAskAboutProject && (
            <button
              onClick={() => onAskAboutProject(project.name)}
              className="text-[11px] text-neutral-300 hover:text-white flex items-center gap-1 bg-white/[0.05] hover:bg-white/[0.1] px-2.5 py-1 rounded transition-colors"
            >
              <Sparkles size={11} className="text-neutral-300" />
              Ask AI about this
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
