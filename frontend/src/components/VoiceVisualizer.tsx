"use client";

import React from "react";

interface VoiceVisualizerProps {
  isActive: boolean;
  color?: string;
  className?: string;
}

export const VoiceVisualizer: React.FC<VoiceVisualizerProps> = ({
  isActive,
  color = "bg-[#f3f3ef]",
  className = "",
}) => {
  return (
    <div className={`flex items-center gap-[3px] h-6 px-1 ${className}`}>
      {[40, 75, 100, 60, 85].map((heightPct, idx) => (
        <span
          key={idx}
          className={`w-[2px] rounded-full transition-all duration-300 ${color} ${
            isActive ? "soundwave-bar opacity-90" : "h-[3px] opacity-30"
          }`}
          style={{
            height: isActive ? `${heightPct}%` : "3px",
            animationDelay: `${idx * 0.15}s`,
          }}
        />
      ))}
    </div>
  );
};

