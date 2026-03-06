"""
SK Framework — Session Manager
Tracks attack sessions and stores results using SQLAlchemy + SQLite.
"""

import json
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import create_engine, Column, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from src.core.config import config
from src.utils.logger import get_logger

log = get_logger("session")

Base = declarative_base()


# ─── ORM Models ───

class AttackSession(Base):
    __tablename__ = "attack_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    module_name = Column(String, nullable=False)
    target_provider = Column(String, nullable=False)
    target_model = Column(String, nullable=False)
    payload = Column(Text)
    response = Column(Text)
    result = Column(String)           # success | partial | failure | unknown
    confidence = Column(Float)
    score = Column(Float)
    signals = Column(Text)            # JSON array of signal strings
    details = Column(Text)
    extra_metadata = Column(Text)     # JSON blob for extra data (renamed from metadata)


# ─── Session Manager ───

class SessionManager:
    """Manages attack session persistence."""

    def __init__(self):
        db_path = config.db.db_path
        # Ensure directory exists
        from pathlib import Path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self.engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        log.info("session_manager_init", db_path=db_path)

    def save(self, attack_result: Any) -> str:
        """
        Save an AttackResult to the database.
        Returns the session ID.
        """
        session_id = str(uuid.uuid4())

        # Support both Pydantic and legacy objects (for transition)
        is_pydantic = hasattr(attack_result, "model_dump")

        with self.Session() as session:
            if is_pydantic:
                record = AttackSession(
                    id=session_id,
                    module_name=attack_result.module,
                    target_provider=attack_result.provider,
                    target_model=attack_result.model,
                    payload=attack_result.payload,
                    response=attack_result.response,
                    result=attack_result.score.result.value,
                    confidence=attack_result.score.confidence,
                    score=attack_result.score.score,
                    signals=json.dumps(attack_result.score.signals),
                    details=attack_result.score.details,
                    extra_metadata=json.dumps(attack_result.metadata),
                )
            else:
                record = AttackSession(
                    id=session_id,
                    module_name=attack_result.module,
                    target_provider=attack_result.provider,
                    target_model=attack_result.model,
                    payload=attack_result.payload,
                    response=attack_result.response,
                    result=attack_result.score.result.value,
                    confidence=attack_result.score.confidence,
                    score=attack_result.score.score,
                    signals=json.dumps(attack_result.score.signals),
                    details=attack_result.score.details,
                    extra_metadata=json.dumps(attack_result.metadata),
                )
            session.add(record)
            session.commit()
            log.info("session_saved", id=session_id, module=attack_result.module)

        return session_id

    def get(self, session_id: str) -> AttackSession | None:
        """Retrieve a session by ID."""
        with self.Session() as session:
            return session.query(AttackSession).filter_by(id=session_id).first()

    def history(self, limit: int = 20, module: str | None = None) -> list[AttackSession]:
        """Get recent attack history, optionally filtered by module."""
        with self.Session() as session:
            q = session.query(AttackSession).order_by(AttackSession.created_at.desc())
            if module:
                q = q.filter_by(module_name=module)
            return q.limit(limit).all()

    def stats(self) -> dict[str, Any]:
        """Get aggregate stats across all sessions."""
        with self.Session() as session:
            total = session.query(AttackSession).count()
            successes = session.query(AttackSession).filter_by(result="success").count()
            failures = session.query(AttackSession).filter_by(result="failure").count()

            return {
                "total_attacks": total,
                "successes": successes,
                "failures": failures,
                "partials": total - successes - failures,
                "success_rate": round(successes / total, 2) if total > 0 else 0.0,
            }
