"use client";

import { cn, formatTime } from "@/lib/utils";
import type { Message } from "@/lib/api";

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={cn(
        "flex gap-3 animate-fade-up",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
    >
      {/* Avatar */}
      {!isUser && (
        <div className="flex-shrink-0 w-9 h-9 rounded-full bg-brand-500 flex items-center justify-center text-lg shadow-sm">
          👨‍🍳
        </div>
      )}

      {/* Bubble */}
      <div
        className={cn(
          "relative max-w-[80%] sm:max-w-[70%] px-4 py-3 rounded-2xl shadow-sm",
          isUser
            ? "bg-brand-500 text-white rounded-tr-sm"
            : "bg-white text-gray-800 rounded-tl-sm border border-gray-100"
        )}
      >
        {/* Render content — support newlines and bullet lists */}
        <div className="prose-chat text-sm leading-relaxed whitespace-pre-wrap break-words">
          {message.content}
        </div>

        {/* Timestamp */}
        {message.timestamp && (
          <div
            className={cn(
              "text-[10px] mt-1.5 select-none",
              isUser ? "text-orange-200 text-right" : "text-gray-400"
            )}
          >
            {formatTime(message.timestamp)}
          </div>
        )}
      </div>
    </div>
  );
}
