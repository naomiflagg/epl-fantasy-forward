"""Squad-related Pydantic schemas."""

from datetime import datetime
from uuid import UUID
from typing import List, Optional, Any
from pydantic import BaseModel, Field


class SquadBase(BaseModel):
    """Base squad schema."""

    players: List[Any] = Field(default_factory=list, description="Array of player objects")
    budget_remaining: float = Field(..., ge=0, description="Remaining budget in millions")
    formation: Optional[str] = Field(None, description="Squad formation (e.g., 4-3-3)")


class SquadCreate(SquadBase):
    """Schema for creating a new squad."""

    pass


class SquadUpdate(BaseModel):
    """Schema for updating an existing squad."""

    players: Optional[List[Any]] = None
    budget_remaining: Optional[float] = Field(None, ge=0)
    formation: Optional[str] = None


class SquadResponse(SquadBase):
    """Schema for squad response."""

    id: UUID
    user_id: UUID
    updated_at: datetime

    class Config:
        from_attributes = True


class TransferSuggestionBase(BaseModel):
    """Base transfer suggestion schema."""

    player_out_id: int
    player_in_id: int
    reasoning: Optional[str] = None
    confidence_score: float = Field(..., ge=0.0, le=1.0)


class TransferSuggestionResponse(TransferSuggestionBase):
    """Schema for transfer suggestion response."""

    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
