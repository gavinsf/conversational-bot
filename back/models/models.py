import enum
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, DateTime, Float
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

class SenderType(enum.Enum):
    customer       = "customer"
    bot            = "bot"
    agent          = "agent"
    system         = "system"

class Priority(enum.Enum):
    low            = "low"
    medium         = "medium"
    high           = "high"

class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("customers.id"))
    last_intent: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[ConversationStatus] = mapped_column(
        SQLEnum(ConversationStatus), default=ConversationStatus.bot_handling
    )
    channel: Mapped[Channel] = mapped_column(
        SQLEnum(Channel), default = Channel.web_chat
    )
    last_intent: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc),
                                            onupdate=datetime.now(timezone.utc))

    customer: Mapped["Customer"] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at"
    )
    escalation: Mapped["EscalationTicket | None"] = relationship(
        back_populates="conversation", uselist=False, cascade="all, delete-orphan"
    )

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[String] = mapped_column(String, nullable=False)
    email: Mapped[String] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan"
    )

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conv_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id"))
    sender: Mapped[SenderType] = mapped_column(SQLEnum(SenderType), nullable=False)
    text: Mapped[String] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    # For bot
    intent: Mapped[String | None] = mapped_column(String)
    confidence: Mapped[Float | None] = mapped_column(Float)

    conversation: Mapped["Conversation"] = mapped_column(
        back_populates="message", cascade="all, delete-orphan"
    )

class EscalationTicket(Base):
    __tablename__ = "escalation_tickets"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id"), unique=True)
    reason: Mapped[String] = mapped_column(String, nullable=False)
    priority: Mapped[Priority] = mapped_column(SQLEnum(Priority))
    assigned_agent: Mapped[String | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    conversation: Mapped["Conversation"] = mapped_column(
        back_populates="escalation_tickets",
    )