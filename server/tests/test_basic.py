import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.database import Base

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")

def test_database_connection(test_db):
    """Test that database connection works"""
    db = TestingSessionLocal()
    try:
        # Simple query to verify connection
        result = db.execute(text("SELECT 1")).fetchone()
        assert result[0] == 1
    finally:
        db.close()

def test_basic_math():
    """Basic sanity test"""
    assert 1 + 1 == 2
    assert 2 * 3 == 6
