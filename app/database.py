"""
Database Configuration
======================
SQLAlchemy database setup with session management.
"""

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# Handle SQLite vs PostgreSQL
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _migrate_columns():
    """
    Add new v2.0 columns to existing tables.
    SQLAlchemy create_all() only creates new tables, not new columns.
    This function checks for missing columns and adds them via ALTER TABLE.
    """
    inspector = inspect(engine)
    
    migrations = []
    
    # Account table: per-account scheduling columns
    if "accounts" in inspector.get_table_names():
        existing = {c["name"] for c in inspector.get_columns("accounts")}
        if "schedule_enabled" not in existing:
            migrations.append("ALTER TABLE accounts ADD COLUMN schedule_enabled BOOLEAN DEFAULT FALSE")
        if "schedule_warmup" not in existing:
            migrations.append("ALTER TABLE accounts ADD COLUMN schedule_warmup BOOLEAN DEFAULT TRUE")
        if "schedule_posting" not in existing:
            migrations.append("ALTER TABLE accounts ADD COLUMN schedule_posting BOOLEAN DEFAULT TRUE")
    
    # ScheduleConfig table: timing columns
    if "schedule_config" in inspector.get_table_names():
        existing = {c["name"] for c in inspector.get_columns("schedule_config")}
        if "warmup_hour_est" not in existing:
            migrations.append("ALTER TABLE schedule_config ADD COLUMN warmup_hour_est INTEGER DEFAULT 8")
        if "video_gen_hour_est" not in existing:
            migrations.append("ALTER TABLE schedule_config ADD COLUMN video_gen_hour_est INTEGER DEFAULT 9")
        if "posting_hours_est" not in existing:
            migrations.append("ALTER TABLE schedule_config ADD COLUMN posting_hours_est VARCHAR(50) DEFAULT '10,13,17'")
    
    if migrations:
        with engine.begin() as conn:
            for sql in migrations:
                try:
                    conn.execute(text(sql))
                except Exception as e:
                    # Column might already exist in some edge cases
                    pass
        print(f"[DB Migration] Applied {len(migrations)} column migrations")


def init_db():
    """Initialize database tables and run migrations."""
    from app.models import account  # noqa: Import models to register them
    Base.metadata.create_all(bind=engine)
    _migrate_columns()

