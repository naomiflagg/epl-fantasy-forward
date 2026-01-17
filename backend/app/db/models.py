"""SQLAlchemy database models."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Text, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    """User model for authentication and profile."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    squads = relationship("UserSquad", back_populates="user", cascade="all, delete-orphan")
    transfer_suggestions = relationship(
        "TransferSuggestion", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class UserSquad(Base):
    """User's fantasy squad with players and budget information."""

    __tablename__ = "user_squads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    players = Column(JSONB, nullable=False, default=list)  # Array of player objects
    budget_remaining = Column(Float, nullable=False, default=100.0)
    formation = Column(String(50), nullable=True)  # e.g., "4-3-3", "3-4-3"
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="squads")

    def __repr__(self) -> str:
        return f"<UserSquad(id={self.id}, user_id={self.user_id}, formation={self.formation})>"


class TransferSuggestion(Base):
    """AI-generated transfer suggestions for users."""

    __tablename__ = "transfer_suggestions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    player_out_id = Column(Integer, nullable=False)  # FPL player ID to transfer out
    player_in_id = Column(Integer, nullable=False)  # FPL player ID to transfer in
    reasoning = Column(Text, nullable=True)  # AI explanation for the transfer
    confidence_score = Column(Float, nullable=False, default=0.0)  # 0.0 to 1.0
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="transfer_suggestions")

    def __repr__(self) -> str:
        return (
            f"<TransferSuggestion(id={self.id}, out={self.player_out_id}, in={self.player_in_id})>"
        )
