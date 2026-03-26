from pydantic import BaseModel, Field
from typing import Optional, List


class Message(BaseModel):
    """A single conversation message."""

    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message text content")
    timestamp: Optional[str] = Field(default=None, description="ISO timestamp")


class ChatRequest(BaseModel):
    """Request body for the /api/chat endpoint."""

    message: str = Field(..., description="The user's current message", min_length=1)
    restaurant_id: str = Field(
        default="default",
        description="Restaurant identifier for multi-tenant support",
    )
    conversation_history: List[Message] = Field(
        default_factory=list,
        description="Full prior conversation for multi-turn memory",
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Session UUID — generated server-side if not provided",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "What are the best sellers?",
                "restaurant_id": "my_restaurant",
                "conversation_history": [],
            }
        }
    }


class ChatResponse(BaseModel):
    """Response body for the /api/chat endpoint."""

    response: str = Field(..., description="AI Waiter's reply")
    conversation_history: List[Message] = Field(
        ..., description="Updated full conversation history"
    )
    session_id: str = Field(..., description="Session UUID")
    is_on_topic: bool = Field(
        default=True,
        description="Whether the question was menu-related",
    )


class UploadResponse(BaseModel):
    """Response body for the /api/upload-menu endpoint."""

    message: str
    items_processed: int
    restaurant_id: str
    status: str = "success"
