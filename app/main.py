from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime, timedelta
import random
from app.schemas import TriggerCreate, TriggerRead, TriggerUpdate


app = FastAPI()

# In-memory storage
triggers = []
archived_triggers = []  # Store archived triggers here
trigger_id_counter = 1

@app.get("/")
def read_root():
    return {"message": "Welcome to the Event Trigger Platform!"}
# Create a new trigger
@app.post("/triggers/", response_model=TriggerRead)
async def create_trigger(request: TriggerCreate):
    global trigger_id_counter
    new_trigger = {"id": trigger_id_counter, "created_at": datetime.utcnow(), **request.dict()}
    triggers.append(new_trigger)
    trigger_id_counter += 1
    return new_trigger

# Read all active triggers
@app.get("/triggers/", response_model=List[TriggerRead])
async def get_all_triggers():
    return triggers

# Read a trigger by ID
@app.get("/triggers/{trigger_id}", response_model=TriggerRead)
async def get_trigger(trigger_id: int):
    trigger = next((t for t in triggers if t["id"] == trigger_id), None)
    if not trigger:
        raise HTTPException(status_code=404, detail="Trigger not found")
    return trigger

# Update a trigger
@app.put("/triggers/{trigger_id}", response_model=TriggerRead)
async def update_trigger(trigger_id: int, request: TriggerUpdate):
    for trigger in triggers:
        if trigger["id"] == trigger_id:
            update_data = request.dict(exclude_unset=True)
            trigger.update(update_data)
            return trigger
    raise HTTPException(status_code=404, detail="Trigger not found")

# Delete a trigger
@app.delete("/triggers/{trigger_id}")
async def delete_trigger(trigger_id: int):
    global triggers
    triggers = [t for t in triggers if t["id"] != trigger_id]
    return {"message": f"Trigger {trigger_id} deleted"}

# Manual Testing Endpoint: Generate Random Test Triggers
@app.post("/triggers/test/manual")
async def manual_testing():
    # Generate a random trigger for testing
    global trigger_id_counter
    test_trigger = {
        "id": trigger_id_counter,
        "name": f"Test Trigger {trigger_id_counter}",
        "trigger_type": random.choice(["scheduled", "api", "time-based"]),
        "schedule_time": None,
        "api_payload": {"message": "This is a test payload"},
        "created_at": datetime.utcnow(),
    }
    triggers.append(test_trigger)
    trigger_id_counter += 1
    return {"message": "Manual test trigger created", "trigger": test_trigger}

# Archive a trigger by ID
@app.post("/triggers/{trigger_id}/archive")
async def archive_trigger(trigger_id: int):
    global triggers, archived_triggers
    trigger = next((t for t in triggers if t["id"] == trigger_id), None)
    if not trigger:
        raise HTTPException(status_code=404, detail="Trigger not found")

    triggers = [t for t in triggers if t["id"] != trigger_id]
    archived_triggers.append(trigger)
    return {"message": f"Trigger {trigger_id} archived", "trigger": trigger}

# View all archived triggers
@app.get("/triggers/archived", response_model=List[TriggerRead])
async def get_archived_triggers():
    return archived_triggers

# Automatic archival of old triggers (older than 30 days)
@app.post("/triggers/archive-old")
async def archive_old_triggers():
    global triggers, archived_triggers
    threshold_date = datetime.utcnow() - timedelta(days=30)
    to_archive = [t for t in triggers if t["created_at"] < threshold_date]
    if not to_archive:
        return {"message": "No triggers older than 30 days to archive"}

    triggers = [t for t in triggers if t["created_at"] >= threshold_date]
    archived_triggers.extend(to_archive)
    return {"message": "Old triggers archived", "archived_count": len(to_archive)}
