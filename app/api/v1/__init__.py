"""API v1 routes."""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, squads

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(squads.router, prefix="/squads", tags=["squads"])
