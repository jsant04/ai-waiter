# 🍽️ AI Waiter – Intelligent Restaurant Assistant

> **Meet your AI Waiter 👋 – ready to answer questions, guide customers, and make service a breeze!**

A fully functional MVP of an AI-powered restaurant assistant built with **Next.js**, **FastAPI**, and **LangGraph Agentic RAG**. Customers can scan a QR code or open a link to instantly chat with an AI that knows the entire menu.

---

## 📁 Project Structure

```
ai-waiter/
├── frontend/          # Next.js App Router (Vercel deployment)
│   ├── app/
│   │   ├── page.tsx           # Landing page
│   │   └── chat/page.tsx      # Chat interface
│   ├── components/
│   │   ├── ChatInterface.tsx
│   │   ├── ChatMessage.tsx
│   │   ├── TypingIndicator.tsx
│   │   ├── QuickReplyButtons.tsx
│   │   ├── QRCodeSection.tsx
│   │   └── ui/                # ShadCN-style UI primitives
│   └── lib/
│       ├── api.ts             # Backend API calls
│       └── utils.ts
│
├── backend/           # FastAPI + LangGraph (Render/Railway deployment)
│   ├── main.py                # FastAPI app entry point
│   ├── agents/
│   │   └── rag_agent.py       # LangGraph RAG workflow
│   ├── routers/
│   │   ├── chat.py            # POST /api/chat
│   │   └── upload.py          # POST /api/upload-menu
│   ├── services/
│   │   ├── menu_parser.py     # Excel → LangChain Documents
│   │   ├── embeddings.py      # OpenAI Embeddings
│   │   └── vector_store.py    # Supabase pgvector
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── supabase/
│   │   └── migrations.sql     # Database setup
│   └── requirements.txt
│
└── sample_menu.xlsx   # Example menu for testing
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- [Supabase](https://supabase.com) account (free tier works)
- [OpenAI API key](https://platform.openai.com)

---

## 🗄️ Step 1 – Supabase Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** and run the SQL in `backend/supabase/migrations.sql`
3. Copy your **Project URL** and **Service Role Key** from **Settings → API**

---

## ⚙️ Step 2 – Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend docs available at: `http://localhost:8000/docs`

### Backend Environment Variables (`.env`)

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Supabase service role key |
| `MODEL_NAME` | LLM model (default: `gpt-4o-mini`) |
| `EMBEDDING_MODEL` | Embeddings model (default: `text-embedding-3-small`) |
| `CORS_ORIGINS` | Allowed origins (comma-separated) |

---

## 🎨 Step 3 – Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with your backend URL

# Run dev server
npm run dev
```

Frontend at: `http://localhost:3000`

### Frontend Environment Variables (`.env.local`)

| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | Backend URL (e.g., `http://localhost:8000`) |
| `NEXT_PUBLIC_RESTAURANT_ID` | Restaurant identifier (default: `default`) |

---

## 🍜 Step 4 – Upload Your Menu

### Excel Menu Format

Create an Excel file (`.xlsx`) with these columns:

| Name | Category | Price | Description | Allergens | Spicy Level | Vegetarian | Vegan |
|------|----------|-------|-------------|-----------|-------------|-----------|-------|
| Margherita Pizza | Pizza | 14.99 | Classic tomato & mozzarella | Gluten, Dairy | None | Yes | No |
| Spicy Chicken Wings | Starters | 12.99 | Crispy wings with hot sauce | None | High | No | No |

**Upload via API:**
```bash
curl -X POST http://localhost:8000/api/upload-menu \
  -F "file=@sample_menu.xlsx" \
  -F "restaurant_id=my_restaurant"
```

**Upload via UI:** Go to `http://localhost:3000` and use the upload section on the landing page.

---

## 🧠 LangGraph RAG Workflow

```
User Question
     │
     ▼
┌─────────────┐
│ check_topic │ ──── Off-topic ──► Friendly redirect
└─────────────┘
     │ On-topic
     ▼
┌──────────────┐
│   retrieve   │  Vector search in Supabase pgvector
└──────────────┘
     │
     ▼
┌──────────────┐
│   generate   │  GPT generates waiter-style answer
└──────────────┘
     │
     ▼
┌──────────────┐
│   improve    │  Refines tone & clarity
└──────────────┘
     │
     ▼
  Response
```

---

## ☁️ Deployment

### Frontend → Vercel

```bash
cd frontend
npm install -g vercel
vercel --prod
```

Set environment variables in **Vercel Dashboard → Project → Settings → Environment Variables:**
- `NEXT_PUBLIC_API_URL` → your Render/Railway backend URL
- `NEXT_PUBLIC_RESTAURANT_ID` → your restaurant ID

### Backend → Render

1. Push your code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render Dashboard

### Backend → Railway

```bash
cd backend
railway init
railway up
```

Add environment variables via `railway variables set KEY=VALUE`

---

## 🧪 Testing the API

```bash
# Health check
curl http://localhost:8000/health

# Chat with the AI Waiter
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the best sellers?",
    "restaurant_id": "default",
    "conversation_history": []
  }'

# Upload menu
curl -X POST http://localhost:8000/api/upload-menu \
  -F "file=@sample_menu.xlsx" \
  -F "restaurant_id=default"
```

---

## 🌟 Features

| Feature | Status |
|---------|--------|
| Conversational chat UI (ChatGPT-like) | ✅ |
| Typing indicator animation | ✅ |
| QR code for mobile access | ✅ |
| Quick-reply buttons | ✅ |
| Excel menu upload | ✅ |
| LangGraph agentic RAG | ✅ |
| Supabase pgvector search | ✅ |
| Multi-turn conversation memory | ✅ |
| Topic validation (off-topic guard) | ✅ |
| Answer quality improvement step | ✅ |
| Mobile-responsive design | ✅ |
| Multi-restaurant support | ✅ |

---

## 🛣️ Roadmap

- [ ] Dashboard for menu management and analytics
- [ ] PDF/image menu parsing
- [ ] Voice input support
- [ ] Popular questions analytics
- [ ] Streaming responses (SSE)
- [ ] Multi-language support

---

## 📄 License

MIT License – feel free to use and modify.
