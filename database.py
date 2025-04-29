# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Get database credentials from environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "replygenius")

# Construct database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine with connection pool
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections after 30 minutes
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionFactory = sessionmaker(bind=engine)

# Create thread-local session
db_session = scoped_session(SessionFactory)

# Import models to ensure they're registered with the Base
from models import Base, Business, PhoneNumber, Customer, Message, ContextItem

def init_db():
    """Initialize the database by creating all tables"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
def get_session():
    """Get a new database session"""
    return SessionFactory()

def setup_pgvector(session):
    """Ensure pgvector extension is enabled"""
    session.execute("CREATE EXTENSION IF NOT EXISTS vector")
    session.commit()