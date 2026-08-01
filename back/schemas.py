from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import uuid


class ChatInput(BaseModel):
    id: str
    text: str


class Message(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    content: Optional[str] = None
    content_type: Optional[str] = Field(default=None, alias="contentType")


class SlotValue(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    original_value: Optional[str] = Field(default=None, alias="originalValue")
    interpreted_value: Optional[str] = Field(default=None, alias="interpretedValue")
    resolved_values: list[str] = Field(default_factory=list, alias="resolvedValues")


class Slot(BaseModel):
    value: Optional[SlotValue] = None


class DialogAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    type: Optional[str] = None
    slot_to_elicit: Optional[str] = Field(default=None, alias="slotToElicit")


class Intent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    slots: dict[str, Optional[Slot]] = Field(default_factory=dict)
    state: Optional[str] = None
    confirmation_state: Optional[str] = Field(default=None, alias="confirmationState")


class SessionState(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    dialog_action: Optional[DialogAction] = Field(default=None, alias="dialogAction")
    intent: Optional[Intent] = None
    session_attributes: Optional[dict[str, str]] = Field(default=None, alias="sessionAttributes")
    originating_request_id: Optional[str] = Field(default=None, alias="originatingRequestId")


class ChatResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    messages: list[Message] = Field(default_factory=list)
    session_state: SessionState = Field(alias="sessionState")
    session_id: Optional[str] = Field(default=None, alias="sessionId")
    confidence_score : Optional[float] = 0