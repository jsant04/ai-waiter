import type { Metadata } from "next";
import { ChatInterface } from "@/components/ChatInterface";
import { ChefHat } from "lucide-react";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Chat – AI Waiter",
  description: "Chat with your AI Waiter to explore the menu and get recommendations.",
};

export default function ChatPage() {
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* ── Top Navigation Bar ── */}
      <header className="flex-shrink-0 bg-white border-b border-gray-100 shadow-sm">
        <div className="max-w-3xl mx-auto px-4 h-14 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 group">
            <ChefHat className="w-6 h-6 text-brand-500 group-hover:scale-110 transition-transform" />
            <span className="font-bold text-gray-900">AI Waiter</span>
          </Link>
          <div className="flex items-center gap-2">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-500" />
            </span>
            <span className="text-sm text-gray-500">Online</span>
          </div>
        </div>
      </header>

      {/* ── Chat Interface (fills remaining height) ── */}
      <div className="flex-1 overflow-hidden max-w-3xl w-full mx-auto">
        <ChatInterface />
      </div>
    </div>
  );
}
