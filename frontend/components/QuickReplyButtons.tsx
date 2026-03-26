interface QuickReply {
  label: string;
  message: string;
  emoji: string;
}

const QUICK_REPLIES: QuickReply[] = [
  { label: "Best sellers",      message: "What are your best sellers?",              emoji: "⭐" },
  { label: "Spicy dishes",      message: "Which dishes are spicy?",                  emoji: "🌶️" },
  { label: "Vegetarian",        message: "What vegetarian options do you have?",     emoji: "🥦" },
  { label: "Vegan options",     message: "Do you have any vegan dishes?",            emoji: "🌱" },
  { label: "Today's specials",  message: "What are today's specials?",               emoji: "✨" },
  { label: "Drinks menu",       message: "What drinks do you serve?",                emoji: "🍹" },
  { label: "Gluten-free",       message: "Do you have gluten-free options?",         emoji: "🌾" },
  { label: "Prices",            message: "Can you tell me about the prices?",        emoji: "💰" },
];

interface QuickReplyButtonsProps {
  onSelect: (message: string) => void;
  disabled?: boolean;
}

export function QuickReplyButtons({ onSelect, disabled }: QuickReplyButtonsProps) {
  return (
    <div className="px-4 py-2">
      <p className="text-xs text-gray-400 mb-2 font-medium">Quick questions</p>
      <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-none">
        {QUICK_REPLIES.map(({ label, message, emoji }) => (
          <button
            key={label}
            onClick={() => onSelect(message)}
            disabled={disabled}
            className="flex-shrink-0 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-brand-200 bg-brand-50 text-brand-700 text-xs font-medium hover:bg-brand-100 hover:border-brand-300 transition-colors disabled:opacity-40 disabled:cursor-not-allowed whitespace-nowrap active:scale-95"
          >
            <span>{emoji}</span>
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}
