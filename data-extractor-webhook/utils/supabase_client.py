"""
Module for initializing and managing Supabase client connection.
"""

import os
from typing import Optional
from supabase import Client, create_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase configuration
SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")

# Validate environment variables
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing required environment variables: SUPABASE_URL or SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
