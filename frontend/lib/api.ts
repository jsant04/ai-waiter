/**
 * AI Waiter – Backend API Client
 * --------------------------------
 * Development  → set NEXT_PUBLIC_API_URL=http://localhost:8000 in .env.local
 * Vercel (monorepo) → leave NEXT_PUBLIC_API_URL unset; requests go to /api/*
 *                     on the same domain via vercel.json routing.
 */

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "";

const RESTAURANT_ID =
  process.env.NEXT_PUBLIC_RESTAURANT_ID ?? "default";

// ── Types ─────────────────────────────────────────────────

export interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

export interface ChatResponse {
  response: string;
  conversation_history: Message[];
  session_id: string;
  is_on_topic: boolean;
}

export interface UploadMenuResponse {
  message: string;
  items_processed: number;
  restaurant_id: string;
  status: string;
}

// ── Helpers ───────────────────────────────────────────────

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const json = await res.json();
      detail = json.detail ?? detail;
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  return res.json() as Promise<T>;
}

// ── API Functions ─────────────────────────────────────────

/**
 * Send a chat message to the AI Waiter.
 *
 * @param message             The user's current text.
 * @param conversationHistory Full prior history for multi-turn memory.
 * @param sessionId           Optional session UUID (auto-generated server-side).
 */
export async function sendMessage(
  message: string,
  conversationHistory: Message[],
  sessionId?: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      restaurant_id: RESTAURANT_ID,
      conversation_history: conversationHistory,
      session_id: sessionId,
    }),
  });
  return handleResponse<ChatResponse>(res);
}

/**
 * Upload an Excel menu file and build the vector index.
 *
 * @param file         The .xlsx / .xls file selected by the user.
 * @param restaurantId Optional override (defaults to RESTAURANT_ID env var).
 */
export async function uploadMenu(
  file: File,
  restaurantId: string = RESTAURANT_ID
): Promise<UploadMenuResponse> {
  const form = new FormData();
  form.append("file", file);
  form.append("restaurant_id", restaurantId);

  const res = await fetch(`${API_URL}/api/upload-menu`, {
    method: "POST",
    body: form,
  });
  return handleResponse<UploadMenuResponse>(res);
}

/**
 * Ping the health endpoint to check backend availability.
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_URL}/health`, { cache: "no-store" });
    return res.ok;
  } catch {
    return false;
  }
}

export { RESTAURANT_ID, API_URL };
