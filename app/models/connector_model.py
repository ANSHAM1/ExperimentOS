from sqlalchemy import (String, DateTime, ForeignKey, func)
from sqlalchemy.orm import Mapped, mapped_column

from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from datetime import datetime

from app.db import Base



class MongoModel(Base):

    __tablename__ = "mongo_connections"

    id            : Mapped[UUID]     = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    user_id       : Mapped[UUID]     = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    uri           : Mapped[str]      = mapped_column(String(500), unique=True, nullable=False)

    created_at    : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())