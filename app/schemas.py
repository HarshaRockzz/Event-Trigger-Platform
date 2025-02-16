from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

# Base schema for common attributes
class TriggerBase(BaseModel):
    name: str = Field(..., example="Test Trigger")
    trigger_type: str = Field(
        ..., title="Trigger Type", pattern="^(scheduled|api|time-based)$", example="api"
    )
    schedule_time: Optional[datetime] = None
    api_payload: Optional[Dict[str, str]] = None

# Schema for creating a new trigger
class TriggerCreate(TriggerBase):
    pass

# Schema for reading a trigger (includes ID)
class TriggerRead(TriggerBase):
    id: int

# Schema for updating a trigger (all fields optional)
class TriggerUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Trigger Name")
    trigger_type: Optional[str] = Field(
        None, title="Trigger Type", pattern="^(scheduled|api|time-based)$", example="api"
    )
    schedule_time: Optional[datetime] = None
    api_payload: Optional[Dict[str, str]] = None

# Schema for logging events
class EventLogCreate(BaseModel):
    trigger_id: int
    event_message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)  # Automatically logs the time
