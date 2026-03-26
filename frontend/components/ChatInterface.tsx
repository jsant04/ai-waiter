"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ChatMessage } from "@/components/ChatMessage";
import { TypingIndicator } from "@/components/TypingIndicator";
import { QuickReplyButtons } from "@/components/QuickReplyButtons";
import { sendMessage, type Message } from "@/lib/api";
import { generateId } from "@/lib/utils";
import { Send, Trash2, RefreshCw } from "lucide-react";

/* ── Welcome message shown before the user sends anything ─── */
const WELCOME_MESSAGE: Message = {
  role: "assistant",
  content:
    "👋 Hello! I'm your AI Waiter. I can help you with:\n\n• Menu questions & recommendations\n• Ingredients & allergens\n• Prices & portions\n• Dietary options (vegetarian, vegan, gluten-free)\n\nWhat can I get for you today?",
  timestamp: new Date().toISOString(),
};

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([WELCOME_MESSAGE]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>(() => generateId());
  const [error, setError] = useState<string | null>(null);

  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  /* ── Auto-scroll to latest message ── */
  useEffect(() => {
    const el = scrollAreaRef.current;
    if (el) {
      el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
    }
  }, [messages, isLoading]);

  /* ── Focus input on mount ── */
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  /* ── Core send function ── */
  const handleSend = useCallback(
    async (text: string) => {
      const trimmed = text.trim();
      if (!trimmed || isLoading) return;

      setInput("");
      setError(null);

      // Add user message optimistically
      const userMsg: Message = {
        role: "user",
        content: trimmed,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMsg]);
      setIsLoading(true);

      try {
        // Build history (exclude the static welcome message)
        const history = messages.filter((m) => m !== WELCOME_MESSAGE);

        const result = await sendMessage(trimmed, history, sessionId);

        // Update session ID from server
        if (result.session_id) {
          setSessionId(result.session_id);
        }

        const aiMsg: Message = {
          role: "assistant",
          content: result.response,
          timestamp: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, aiMsg]);
      } catch (err: unknown) {
        const errorText =
          err instanceof Error
            ? err.message
            : "Something went wrong. Please try again.";
        setError(errorText);

        // Show error as assistant message
        const errorMsg: Message = {
          role: "assistant",
          content: `⚠️ ${errorText}`,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, errorMsg]);
      } finally {
        setIsLoading(false);
        // Re-focus input after response
        setTimeout(() => inputRef.current?.focus(), 100);
      }
    },
    [isLoading, messages, sessionId]
  );

  /* ── Form submit ── */
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSend(input);
  };

  /* ── Clear conversation ── */
  const handleClear = () => {
    setMessages([WELCOME_MESSAGE]);
    setSessionId(generateId());
    setError(null);
    setInput("");
    inputRef.current?.focus();
  };

  /* ── Quick reply selection ── */
  const handleQuickReply = (message: string) => {
    handleSend(message);
  };

  const canSend = input.trim().length > 0 && !isLoading;

  return (
    <div className="flex flex-col h-full bg-white">
      {/* ── Toolbar ── */}
      <div className="flex-shrink-0 flex items-center justify-between px-4 py-2 border-b border-gray-100 bg-gray-50/60">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-brand-500 flex items-center justify-center text-base">
            👨‍🍳
          </div>
          <div>
            <p className="text-sm font-semibold text-gray-800">AI Waiter</p>
            <p className="text-xs text-gray-400">
              {isLoading ? "Thinking…" : "Ready to help"}
            </p>
          </div>
        </div>
        <button
          onClick={handleClear}
          title="Clear conversation"
          className="flex items-center gap-1 px-2 py-1 rounded-lg text-xs text-gray-400 hover:text-red-500 hover:bg-red-50 transition-colors"
        >
          <Trash2 className="w-3.5 h-3.5" />
          Clear
        </button>
      </div>

      {/* ── Messages Area ── */}
      <div
        ref={scrollAreaRef}
        className="flex-1 overflow-y-auto px-4 py-4 space-y-4 scroll-smooth"
      >
        {messages.map((msg, i) => (
          <ChatMessage key={`${msg.timestamp}-${i}`} message={msg} />
        ))}

        {/* Typing indicator */}
        {isLoading && <TypingIndicator />}

        {/* Error banner */}
        {error && !isLoading && (
          <div className="flex items-center gap-2 px-4 py-2 bg-red-50 border border-red-100 rounded-xl text-sm text-red-600">
            <RefreshCw className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}
      </div>

      {/* ── Quick Replies ── */}
      <div className="flex-shrink-0 border-t border-gray-100">
        <QuickReplyButtons onSelect={handleQuickReply} disabled={isLoading} />
      </div>

      {/* ── Input Bar ── */}
      <div className="flex-shrink-0 px-4 pb-4 pt-2 border-t border-gray-100 bg-white">
        <form onSubmit={handleSubmit} className="flex gap-2 items-end">
          <Input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about our menu…"
            disabled={isLoading}
            className="flex-1 rounded-xl border-gray-200 focus-visible:ring-brand-500"
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend(input);
              }
            }}
            maxLength={500}
          />
          <Button
            type="submit"
            size="icon"
            disabled={!canSend}
            className="w-10 h-10 flex-shrink-0 rounded-xl"
            aria-label="Send message"
          >
            {isLoading ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </form>
        <p className="text-center text-[10px] text-gray-300 mt-2">
          AI Waiter · Powered by LangGraph RAG
        </p>
      </div>
    </div>
  );
}
