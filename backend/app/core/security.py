"""Security functions for authentication and authorization using Supabase."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.supabase_client import supabase_publishable
from app.db.database import get_db
from app.db.models import User

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Get the current authenticated user from Supabase JWT token.

    Args:
        credentials: HTTP Bearer token credentials from Supabase
        db: Database session

    Returns:
        The authenticated User object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        
        # Verify token with Supabase
        auth_response = supabase_publishable.auth.get_user(token)
        
        if not auth_response or not auth_response.user:
            raise credentials_exception
        
        user_id = auth_response.user.id

    except Exception as e:
        raise credentials_exception

    # Get user from database (Supabase manages auth, we manage app data)
    result = await db.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalar_one_or_none()

    # If user doesn't exist in our database yet, create them
    if user is None:
        user = User(
            id=UUID(user_id),
            email=auth_response.user.email,
            hashed_password=""  # Not used with Supabase auth
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user

