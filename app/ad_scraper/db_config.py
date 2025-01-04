from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base  # Ensure Base is defined in models.py

# Database connection URL (change this with your credentials)
DATABASE_URL = "postgresql://adscraperx_owner:1mYZWdiKO6tJ@ep-ancient-union-a5ivb14v.us-east-2.aws.neon.tech/adscraperx?sslmode=require"

# Create engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_session():
    return SessionLocal()