import type { Metadata, Viewport } from "next";
import "./globals.css";

export const viewport: Viewport = {
  themeColor: "#0b0c0e",
  width: "device-width",
  initialScale: 1,
};

export const metadata: Metadata = {
  title: "AI Chatbot — Interactive Story & Context-Aware Voice Agent",
  description: "An interactive, context-aware AI voice chatbot and narrative assessment experience representing Victorraj — exploring projects like QFoundry, Vic-NLP, and engineering philosophy.",
  authors: [{ name: "Victorraj" }],
  keywords: ["AI Engineer", "Generative AI", "Quantum Computing", "QFoundry", "FastAPI", "Next.js", "Voice AI", "RAG"],
  openGraph: {
    title: "AI Chatbot — Interactive Story & Voice Agent",
    description: "Explore the journey, engineering projects, and thinking behind Victorraj through an interactive 5-chapter story and grounded AI voice agent.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "AI Chatbot — Interactive Story & Voice Agent",
    description: "An interactive AI voice experience and narrative journey exploring engineering projects and systems design.",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark h-full antialiased">
      <body className="min-h-full flex flex-col bg-[#0c0d10] text-[#f3f3ef]">
        {children}
      </body>
    </html>
  );
}
