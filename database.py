import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/coffee",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DatabaseConnectionError(Exception):
    """Raised when the application cannot connect to PostgreSQL."""


GUIDANCE_MESSAGE = f"""
Unable to connect to PostgreSQL using DATABASE_URL="{DATABASE_URL}".

What to do next:
- Ensure PostgreSQL is running and accessible at localhost:5432.
- If your database is not on localhost:5432, set DATABASE_URL before running the app or seed script.
  PowerShell: $env:DATABASE_URL="postgresql://<user>:<password>@<host>:<port>/<database>"
  cmd.exe:    set DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
- Confirm the database name, user, and password exist and match the values used in DATABASE_URL.
"""


def verify_database_connection():
    """Verify that PostgreSQL is reachable and raise a guided error if not."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:  # pragma: no cover - guardrail for runtime environments
        raise DatabaseConnectionError(GUIDANCE_MESSAGE) from exc
