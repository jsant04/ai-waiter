export function TypingIndicator() {
  return (
    <div className="flex gap-3">
      {/* Avatar */}
      <div className="flex-shrink-0 w-9 h-9 rounded-full bg-brand-500 flex items-center justify-center text-lg shadow-sm">
        👨‍🍳
      </div>

      {/* Bubble with animated dots */}
      <div className="bg-white border border-gray-100 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm flex items-center gap-1.5">
        <span
          className="typing-dot w-2 h-2 rounded-full bg-gray-400"
          style={{ animationDelay: "0ms" }}
        />
        <span
          className="typing-dot w-2 h-2 rounded-full bg-gray-400"
          style={{ animationDelay: "200ms" }}
        />
        <span
          className="typing-dot w-2 h-2 rounded-full bg-gray-400"
          style={{ animationDelay: "400ms" }}
        />
      </div>
    </div>
  );
}
