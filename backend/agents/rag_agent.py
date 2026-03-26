"""
LangGraph Agentic RAG Workflow
-------------------------------
Implements a 4-node graph that powers the AI Waiter:

  check_topic ──► retrieve ──► generate ──► improve ──► END
        │
        └─── (off-topic) ──► END  (friendly redirect message)

Node descriptions
-----------------
  check_topic : Uses the LLM to classify whether the user's question
                is about the restaurant menu. Prevents off-topic answers.
  retrieve    : Performs a cosine-similarity search in Supabase pgvector
                to fetch the most relevant menu items.
  generate    : Uses the retrieved context + conversation history to
                produce a warm, waiter-style answer.
  improve     : Refines the answer's tone and structure without adding
                new information (hallucination guard).
"""

import logging
import os
from typing import List, TypedDict

from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from services.vector_store import search_menu

logger = logging.getLogger(__name__)

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

# ── Agent State ───────────────────────────────────────────


class AgentState(TypedDict):
    """Shared state threaded through every node in the graph."""

    question: str
    conversation_history: List[dict]  # [{"role": "user"|"assistant", "content": str}]
    context: str           # retrieved menu snippets (set by retrieve node)
    answer: str            # first-draft answer (set by generate node)
    improved_answer: str   # refined answer (set by improve node)
    is_on_topic: bool      # classification result (set by check_topic node)
    restaurant_id: str


# ── LLM factory ──────────────────────────────────────────

def _llm(temperature: float = 0.7) -> ChatOpenAI:
    return ChatOpenAI(
        model=MODEL_NAME,
        temperature=temperature,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )


# ── Helpers ───────────────────────────────────────────────

def _format_history(history: List[dict], max_turns: int = 6) -> str:
    """Format the last N turns of conversation for LLM context."""
    if not history:
        return "No previous conversation."
    lines = []
    for msg in history[-max_turns:]:
        speaker = "Customer" if msg["role"] == "user" else "AI Waiter"
        lines.append(f"{speaker}: {msg['content']}")
    return "\n".join(lines)


# ── Nodes ─────────────────────────────────────────────────

def check_topic(state: AgentState) -> dict:
    """
    Classify whether the user's question is menu-related.
    Returns: {"is_on_topic": bool}
    """
    llm = _llm(temperature=0.0)

    system = SystemMessage(content="""You are a strict binary classifier for a restaurant AI assistant.

Determine if the user's question is related to:
  - Restaurant menu items, dishes, or drinks
  - Food ingredients, allergens, or dietary info
  - Prices, portion sizes, or availability
  - Restaurant services (e.g. takeaway, reservations)

Reply with ONLY the word "yes" or "no". No explanation.""")

    human = HumanMessage(
        content=f"Is this question about the restaurant's menu or food? '{state['question']}'"
    )

    response = llm.invoke([system, human])
    is_on_topic = "yes" in response.content.strip().lower()

    logger.info(
        "Topic check → '%s' : %s",
        state["question"],
        "ON-TOPIC" if is_on_topic else "OFF-TOPIC",
    )
    return {"is_on_topic": is_on_topic}


def retrieve_documents(state: AgentState) -> dict:
    """
    Fetch the top-5 most relevant menu items from Supabase.
    Returns: {"context": str}
    """
    docs = search_menu(
        query=state["question"],
        restaurant_id=state["restaurant_id"],
        k=5,
    )

    if docs:
        context = "\n\n---\n\n".join(doc.page_content for doc in docs)
    else:
        context = "No specific menu items found matching this query."

    logger.info(
        "Retrieved %d documents for query='%s'", len(docs), state["question"]
    )
    return {"context": context}


def generate_answer(state: AgentState) -> dict:
    """
    Generate a waiter-style answer using retrieved menu context.
    Returns: {"answer": str}
    """
    llm = _llm(temperature=0.7)

    system = SystemMessage(content="""You are a friendly, professional AI Waiter at a restaurant.

Your job:
  - Answer the customer's question using ONLY the provided menu information.
  - Be warm, welcoming, and concise (2–4 sentences max for simple questions).
  - When listing dishes, use this exact format for each item:
      - **Dish Name** - description or details
  - If a dish is not in the context, honestly say you don't have that info.
  - NEVER invent prices, ingredients, or dishes not in the menu data.
  - End with a helpful follow-up offer when appropriate.""")

    human = HumanMessage(content=f"""Menu Information:
{state['context']}

Previous Conversation:
{_format_history(state['conversation_history'])}

Customer's Question: {state['question']}

Please provide a helpful, friendly answer as the AI Waiter.""")

    response = llm.invoke([system, human])
    return {"answer": response.content}


def improve_answer(state: AgentState) -> dict:
    """
    Polish the draft answer for tone and readability.
    Returns: {"improved_answer": str}
    """
    llm = _llm(temperature=0.3)

    system = SystemMessage(content="""You are an expert customer-service editor.

Improve the given restaurant waiter response to be:
  1. Friendly and warm — like a great server at a nice restaurant
  2. Concise — remove redundancy, keep it punchy
  3. Well-structured — when listing dishes use: - **Dish Name** - description
  4. Professional yet approachable

⚠️ Do NOT add new information. Do NOT change facts. Only improve presentation and tone.
⚠️ Always keep dish names in **bold** followed by a dash and the description.
Return only the improved response text, nothing else.""")

    human = HumanMessage(
        content=f"Improve this waiter response:\n\n{state['answer']}"
    )

    response = llm.invoke([system, human])
    return {"improved_answer": response.content}


# ── Routing ───────────────────────────────────────────────

def route_after_topic_check(state: AgentState) -> str:
    """Route to retrieve if on-topic, otherwise end early."""
    return "retrieve" if state.get("is_on_topic") else "__end__"


# ── Graph Assembly ────────────────────────────────────────

def build_rag_graph():
    """Build, wire, and compile the LangGraph RAG workflow."""
    workflow = StateGraph(AgentState)

    workflow.add_node("check_topic", check_topic)
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("generate", generate_answer)
    workflow.add_node("improve", improve_answer)

    workflow.set_entry_point("check_topic")

    workflow.add_conditional_edges(
        "check_topic",
        route_after_topic_check,
        {"retrieve": "retrieve", "__end__": END},
    )
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "improve")
    workflow.add_edge("improve", END)

    return workflow.compile()


# Compile once at import time so all requests share the same graph object.
rag_graph = build_rag_graph()

OFF_TOPIC_REPLY = (
    "I'm here to help you with our menu! 🍽️ "
    "Feel free to ask about our dishes, ingredients, allergens, prices, "
    "or any dietary options. Is there something from our menu I can help with?"
)


# ── Public API ────────────────────────────────────────────

async def run_rag_agent(
    question: str,
    restaurant_id: str,
    conversation_history: List[dict],
) -> dict:
    """
    Run the full agentic RAG pipeline and return the final response.

    Returns:
        {"response": str, "is_on_topic": bool}
    """
    initial_state: AgentState = {
        "question": question,
        "conversation_history": conversation_history,
        "context": "",
        "answer": "",
        "improved_answer": "",
        "is_on_topic": False,
        "restaurant_id": restaurant_id,
    }

    final_state: AgentState = await rag_graph.ainvoke(initial_state)

    is_on_topic: bool = final_state.get("is_on_topic", False)

    if is_on_topic:
        response = (
            final_state.get("improved_answer")
            or final_state.get("answer")
            or "I'm not sure about that. Could you rephrase your question?"
        )
    else:
        response = OFF_TOPIC_REPLY

    return {"response": response, "is_on_topic": is_on_topic}
