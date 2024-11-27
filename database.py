from functools import lru_cache
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config


@lru_cache
def get_settings():
    """
    Retrieve the application settings using an LRU cache for optimization.
    """
    return config.Settings()


# Load database settings
settings = get_settings()
encoded_username = quote_plus(
    settings.cr_db_username
)  # Encode the username to handle special characters.
encoded_password = quote_plus(
    settings.cr_db_password
)  # Encode the password to handle special characters.

# Construct the SQLAlchemy database URL for MySQL
SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{encoded_username}:{encoded_password}"
    f"@{settings.cr_db_host}:{settings.cr_db_port}/{settings.cr_db_name}"
)

# Create a database engine with connection pooling
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Define a session maker for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db_connection():
    """
    Dependency for FastAPI routes to provide a scoped database session.
    Closes the session after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
