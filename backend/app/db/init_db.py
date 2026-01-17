"""Database initialization script."""

import asyncio
from app.db.database import engine, Base
from app.db.models import User, UserSquad, TransferSuggestion


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        # Drop all tables (use with caution in production!)
        # await conn.run_sync(Base.metadata.drop_all)
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
