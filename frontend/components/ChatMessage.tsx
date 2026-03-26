"use client";

import { cn, formatTime } from "@/lib/utils";
import type { Message } from "@/lib/api";

interface ChatMessageProps {
  message: Message;
}

/** Render a single line, converting **text** to <strong>text</strong> */
function renderInline(line: string): React.ReactNode[] {
  const parts = line.split(/(\*\*[^*]+\*\*)/);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    return part;
  });
}

/** Split content into lines and render each one */
function renderContent(content: string) {
  const lines = content.split("\n");
  return lines.map((line, i) => {
    const trimmed = line.trimStart();
    const isListItem = trimmed.startsWith("- ") || trimmed.startsWith("• ");

    if (isListItem) {
      const text = trimmed.slice(2);
      return (
        <div key={i} className="flex gap-1.5 my-0.5">
          <span className="mt-[2px] shrink-0 text-brand-500">•</span>
          <span>{renderInline(text)}</span>
        </div>
      );
    }

    if (trimmed === "") {
      return <div key={i} className="h-1" />;
    }

    return <div key={i}>{renderInline(line)}</div>;
  });
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
        <div className="text-sm leading-relaxed break-words">
          {renderContent(message.content)}
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
