import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "AI Waiter – Your Intelligent Restaurant Assistant",
    template: "%s | AI Waiter",
  },
  description:
    "Meet your AI Waiter – ready to answer menu questions, guide customers, and make service a breeze!",
  keywords: [
    "AI waiter",
    "restaurant assistant",
    "menu chatbot",
    "food ordering",
    "restaurant AI",
  ],
  openGraph: {
    title: "AI Waiter 👋",
    description: "Your friendly AI restaurant assistant — powered by LangGraph RAG.",
    type: "website",
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased bg-white text-gray-900">{children}</body>
    </html>
  );
}
