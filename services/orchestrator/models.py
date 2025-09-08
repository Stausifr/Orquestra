"""Database models for orchestrator."""
from __future__ import annotations

import datetime as dt
import os
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./orq.db")
engine = create_engine(DATABASE_URL, future=True)


class Base(DeclarativeBase):
    pass


class Agent(Base):
    __tablename__ = "agents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    last_refreshed: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)


class Workflow(Base):
    __tablename__ = "workflows"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String, default="pending")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)


class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"))
    status: Mapped[str] = mapped_column(String, default="pending")
    reason: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    workflow: Mapped[Workflow] = relationship()


class CostRecord(Base):
    __tablename__ = "costs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"))
    step: Mapped[str] = mapped_column(String)
    cost: Mapped[float] = mapped_column()


Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
