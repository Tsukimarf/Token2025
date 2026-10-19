"""
src/database.py

Database connection and session management.

Uses SQLAlchemy and defaults to a local SQLite file so the project
runs out of the box with no extra setup. To use a different database
(PostgreSQL, MySQL, etc.), just set the DATABASE_URL environment
variable, e.g.:

    export DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
    export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/mydb"

Install dependencies:
    pip install sqlalchemy python-dotenv
    # plus a driver for your DB, e.g.:
    pip install psycopg2-binary   # for PostgreSQL
    pip install pymysql           # for MySQL
"""

import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv is optional; env vars can still be set manually
    pass

# --- Configuration -----------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# SQLite needs this extra arg when used with multiple threads
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# --- Engine & Session ---------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,          # set True to log all SQL statements
    pool_pre_ping=True,  # auto-reconnect on stale connections
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models to inherit from
Base = declarative_base()


def init_db() -> None:
    """Create all tables defined on models that inherit from Base.

    Call this once at application startup, after importing your models.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI-style dependency: yields a session and closes it afterward.

    Example:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope():
    """Context manager for plain scripts (outside a web framework).

    Example:
        with session_scope() as db:
            db.add(SomeModel(name="example"))
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Quick manual check: creates the tables and confirms connection works
    init_db()
    print(f"Connected to: {DATABASE_URL}")
    print("Tables created (if any models were imported before this ran).")
