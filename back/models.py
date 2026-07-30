import enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from back.database import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid

class ConversationStatus(enum.Enum):
    bot_handling   = "bot_handling"
    agent_handling = "agent_handling"
    escalated      = "escalated"
    resolved       = "resolved"

class Channel(enum.Enum):
    web_chat       = "web_chat"
    voice          = "mobile"
    sms            = "sms"

class Conversation(Base):
    __tablename__ = "conversation"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id : Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"))
    last_intent : Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[ConversationStatus] = mapped_column(
        SQLEnum(ConversationStatus), default=ConversationStatus.bot_handling
    )
    channel: Mapped[Channel] = mapped_column(
        SQLEnum.Channel, default = Channel.web_chat
    )
    last_intent: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    up_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc),
                                            onupdate=datetime.now(timezone.utc))

    customer: Mapped["Customer"] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at"
    )
    escalation: Mapped["EscalationTicket | None"] = relationship(
        back_populates="conversation", uselist=False, cascade="all, delete-orphan"
    )