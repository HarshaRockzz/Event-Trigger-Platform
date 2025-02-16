from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Trigger(Base):
    __tablename__ = "triggers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    trigger_type = Column(String)  # "scheduled" or "api"
    schedule_time = Column(DateTime, nullable=True)
    api_payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class EventLog(Base):
    __tablename__ = "event_logs"
    id = Column(Integer, primary_key=True, index=True)
    trigger_id = Column(Integer)
    event_time = Column(DateTime, default=datetime.utcnow)  # Automatically logs the timestamp
    event_type = Column(String)
    payload = Column(JSON, nullable=True)
    archived = Column(Boolean, default=False)
