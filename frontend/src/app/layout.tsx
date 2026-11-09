import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Chatbot — Interactive Story & Context-Aware Voice Agent",
  description: "An interactive, context-aware AI voice chatbot and narrative assessment experience.",
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
