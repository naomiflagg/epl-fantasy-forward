"""Supabase client initialization."""

from supabase import create_client, Client
from app.core.config import settings

# Initialize Supabase client with secret key for backend operations
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SECRET_KEY)

# For auth verification, we'll use the publishable key client
supabase_publishable: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_PUBLISHABLE_KEY)
