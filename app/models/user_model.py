from sqlalchemy import (String, Text, Enum as SqlEnum, Boolean, DateTime, func)
from sqlalchemy.orm import Mapped, mapped_column

from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from datetime import datetime
from enum import Enum

from app.db import Base



class Role(Enum):
    ADMIN = "ADMIN"
    USER  = "USER"



class User(Base):
    __tablename__ = "users"

    id            : Mapped[UUID]     = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    email         : Mapped[str]      = mapped_column(String(100), unique=True, nullable=False)
    
    password_hash : Mapped[str]      = mapped_column(Text, nullable=False)

    role          : Mapped[Role]     = mapped_column(SqlEnum(Role), nullable=False, default=Role.USER)

    is_active     : Mapped[bool]     = mapped_column(Boolean, nullable=False, default=False)

    created_at    : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    updated_at    : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())