"""Squad management endpoints."""

from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.security import get_current_user
from app.db.database import get_db
from app.db.models import User, UserSquad
from app.schemas.squad import SquadCreate, SquadUpdate, SquadResponse

router = APIRouter()


@router.get("/", response_model=Optional[SquadResponse])
async def get_user_squad(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
) -> Optional[SquadResponse]:
    """
    Get the current user's squad.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        User's squad or None if no squad exists
    """
    result = await db.execute(
        select(UserSquad)
        .where(UserSquad.user_id == current_user.id)
        .order_by(UserSquad.updated_at.desc())
        .limit(1)
    )
    squad = result.scalar_one_or_none()

    if squad:
        return SquadResponse.model_validate(squad)
    return None


@router.post("/", response_model=SquadResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_squad(
    squad_data: SquadCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SquadResponse:
    """
    Create a new squad or update existing squad for the current user.

    Args:
        squad_data: Squad data (players, budget, formation)
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created or updated squad
    """
    # Check if user already has a squad
    result = await db.execute(
        select(UserSquad)
        .where(UserSquad.user_id == current_user.id)
        .order_by(UserSquad.updated_at.desc())
        .limit(1)
    )
    existing_squad = result.scalar_one_or_none()

    if existing_squad:
        # Update existing squad
        existing_squad.players = squad_data.players
        existing_squad.budget_remaining = squad_data.budget_remaining
        existing_squad.formation = squad_data.formation

        await db.commit()
        await db.refresh(existing_squad)
        return SquadResponse.model_validate(existing_squad)
    else:
        # Create new squad
        new_squad = UserSquad(
            user_id=current_user.id,
            players=squad_data.players,
            budget_remaining=squad_data.budget_remaining,
            formation=squad_data.formation,
        )

        db.add(new_squad)
        await db.commit()
        await db.refresh(new_squad)
        return SquadResponse.model_validate(new_squad)


@router.put("/{squad_id}", response_model=SquadResponse)
async def update_squad(
    squad_id: UUID,
    squad_data: SquadUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SquadResponse:
    """
    Update a specific squad by ID.

    Args:
        squad_id: UUID of the squad to update
        squad_data: Updated squad data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated squad

    Raises:
        HTTPException: If squad not found or user doesn't own the squad
    """
    # Get squad
    result = await db.execute(select(UserSquad).where(UserSquad.id == squad_id))
    squad = result.scalar_one_or_none()

    if not squad:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Squad not found")

    # Verify ownership
    if squad.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this squad"
        )

    # Update fields if provided
    if squad_data.players is not None:
        squad.players = squad_data.players
    if squad_data.budget_remaining is not None:
        squad.budget_remaining = squad_data.budget_remaining
    if squad_data.formation is not None:
        squad.formation = squad_data.formation

    await db.commit()
    await db.refresh(squad)

    return SquadResponse.model_validate(squad)
