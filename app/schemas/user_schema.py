from sqlalchemy import (String, Text, Enum as SqlEnum, Boolean, DateTime)
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime, timezone
from enum import Enum

from app.db import Base



class Role(Enum):
    ADMIN = "ADMIN"
    USER  = "USER"



class User(Base):
    __tablename__ = "users"

    id            : Mapped[int]      = mapped_column(primary_key=True)

    email         : Mapped[str]      = mapped_column(String(100), index=True, nullable=False)
    
    password_hash : Mapped[str]      = mapped_column(Text, nullable=False)

    role          : Mapped[Role]     = mapped_column(SqlEnum(Role))

    is_active     : Mapped[bool]     = mapped_column(Boolean, default=True)

    created_at    : Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))