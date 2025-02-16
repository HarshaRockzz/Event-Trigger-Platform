from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.database import get_db
from app.models import Trigger, EventLog
from app.schemas import TriggerCreate, EventLogCreate
from app.tasks import schedule_event
from app.cache import cache_get, cache_set

router = APIRouter()

# Create a new trigger
@router.post("/triggers/")
async def create_trigger(trigger: TriggerCreate, db: AsyncSession = Depends(get_db)):
    new_trigger = Trigger(
        name=trigger.name,
        trigger_type=trigger.trigger_type,
        schedule_time=trigger.schedule_time,
        api_payload=trigger.api_payload,
    )

    db.add(new_trigger)
    await db.flush()
    await db.commit()
    await db.refresh(new_trigger)

    if trigger.trigger_type == "scheduled" and trigger.schedule_time:
        schedule_event.apply_async(eta=trigger.schedule_time, args=[new_trigger.id])

    # Log trigger creation
    event_log = EventLog(
        trigger_id=new_trigger.id,
        event_time=datetime.utcnow(),
        event_type="trigger_created",
        payload={"message": f"Trigger '{new_trigger.name}' created"},
        archived=False,
    )
    db.add(event_log)
    await db.commit()

    return {"message": "Trigger created", "trigger_id": new_trigger.id}

@router.get("/logs/")
async def get_logs(db: AsyncSession = Depends(get_db), filter_last_2_hours: bool = False):
    cache_data = cache_get("logs")
    if cache_data:
        return cache_data

    query = select(EventLog).where(EventLog.archived == False)
    if filter_last_2_hours:
        two_hours_ago = datetime.utcnow() - timedelta(hours=2)
        query = query.where(EventLog.event_time >= two_hours_ago)

    result = await db.execute(query)
    logs = result.scalars().all()

    cache_set("logs", logs, expiry=600)  
    return logs

# Manual trigger test
@router.post("/triggers/test/")
async def manual_test_trigger(trigger_id: int, db: AsyncSession = Depends(get_db)):
    """
    Simulates triggering an event manually for a given trigger ID.
    """
    # Check if the trigger exists
    result = await db.execute(select(Trigger).where(Trigger.id == trigger_id))
    trigger = result.scalar_one_or_none()
    if not trigger:
        raise HTTPException(status_code=404, detail="Trigger not found")


    manual_event_log = EventLog(
        trigger_id=trigger_id,
        event_time=datetime.utcnow(),
        event_type="manual_test",
        payload=trigger.api_payload,
        archived=False,
    )
    db.add(manual_event_log)
    await db.commit()

    return {"message": "Manual trigger test event logged", "trigger_id": trigger_id}

@router.post("/logs/retention/")
async def archive_old_logs(db: AsyncSession = Depends(get_db)):
    """
    Archives logs older than 7 days.
    """
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    result = await db.execute(
        select(EventLog).where(EventLog.event_time < seven_days_ago, EventLog.archived == False)
    )
    old_logs = result.scalars().all()

    if not old_logs:
        return {"message": "No logs older than 7 days found"}

    for log in old_logs:
        log.archived = True

    await db.commit()
    return {"message": f"Archived {len(old_logs)} logs older than 7 days"}

@router.get("/triggers/archived")
async def get_archived_triggers(db: AsyncSession = Depends(get_db)):
    """
    Fetches all archived triggers.
    """
    result = await db.execute(select(Trigger).where(Trigger.archived == True))
    archived_triggers = result.scalars().all()
    return archived_triggers

@router.get("/triggers/{trigger_id}")
async def get_trigger(trigger_id: int, db: AsyncSession = Depends(get_db)):
    """
    Fetches a trigger by its ID.
    """
    result = await db.execute(select(Trigger).where(Trigger.id == trigger_id))
    trigger = result.scalar_one_or_none()
    if not trigger:
        raise HTTPException(status_code=404, detail="Trigger not found")
    return trigger
