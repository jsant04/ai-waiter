"""
Chat Router
-----------
POST /api/chat
  Accepts a user message plus conversation history.
  Runs the LangGraph RAG pipeline and returns the AI Waiter's reply.
"""

import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from agents.rag_agent import run_rag_agent
from models.schemas import ChatRequest, ChatResponse, Message

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with the AI Waiter",
    description=(
        "Send a message to the AI Waiter. Include the full conversation history "
        "for multi-turn memory. The agent validates the topic, retrieves relevant "
        "menu items from the vector store, and returns a refined, waiter-style answer."
    ),
)
async def chat(request: ChatRequest) -> ChatResponse:
    """AI Waiter chat endpoint powered by LangGraph Agentic RAG."""

    session_id = request.session_id or str(uuid.uuid4())
    timestamp = datetime.now(tz=timezone.utc).isoformat()

    logger.info(
        "Chat | session=%s | restaurant=%s | message='%s'",
        session_id,
        request.restaurant_id,
        request.message[:80],
    )

    try:
        # Convert Pydantic Message objects → plain dicts for the agent
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in request.conversation_history
        ]

        # ── Run LangGraph pipeline ──
        result = await run_rag_agent(
            question=request.message,
            restaurant_id=request.restaurant_id,
            conversation_history=history,
        )

        ai_response: str = result["response"]
        is_on_topic: bool = result.get("is_on_topic", True)

        # ── Build updated history ──
        updated_history = list(request.conversation_history)
        updated_history.append(
            Message(role="user", content=request.message, timestamp=timestamp)
        )
        updated_history.append(
            Message(role="assistant", content=ai_response, timestamp=timestamp)
        )

        return ChatResponse(
            response=ai_response,
            conversation_history=updated_history,
            session_id=session_id,
            is_on_topic=is_on_topic,
        )

    except Exception as exc:
        logger.error("Chat pipeline error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="The AI Waiter encountered an error. Please try again.",
        ) from exc
