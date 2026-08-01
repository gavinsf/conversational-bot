import enum
from back.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class MessageLog(Base):
    session_id: Mapped[str] = mapped_column(str, nullable=False)
    text      : Mapped[str] = mapped_column(str, nullable=False)