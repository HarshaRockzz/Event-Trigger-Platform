# Event Trigger Platform

This project is a scalable Event Trigger Platform built using **FastAPI**, **PostgreSQL**, **Redis**, **Celery**, and **Docker**. It supports CRUD operations for triggers and events, retention policies, and manual testing through a user-friendly interface.

Deployed Application: [Event Trigger Platform](https://event-trigger-platform-7svu.onrender.com/docs)

## Features
- **Event Triggers**: Create and manage event triggers (scheduled or API-based).
- **CRUD Operations**: Full Create, Read, Update, Delete support for events and triggers.
- **Retention Policies**: Retain or archive old events for efficient data handling.
- **Manual Testing**: Easily test event triggers manually.
- **Dockerized Services**: Fully containerized using Docker Compose.

## Table of Contents
- [Project Setup](#project-setup)
- [Project Structure](#project-structure)
- [CRUD Operations](#crud-operations)
- [Event Retention](#event-retention)
- [Manual Testing](#manual-testing)
- [Running the Project](#running-the-project)
- [Deployment](#deployment)
- [Example API Requests](#example-api-requests)
- [Production Cost Estimation](#production-cost-estimation)

---

## Project Setup

### Step 1: Create the Project Folder
```sh
mkdir event-trigger-platform
cd event-trigger-platform
```

### Step 2: Create and Activate a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
```

### Step 3: Install Dependencies
```sh
pip install fastapi uvicorn celery redis sqlalchemy asyncpg alembic psycopg2-binary passlib pyjwt python-dotenv docker-compose
```

## Project Structure
```plaintext
event-trigger-platform/
│── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   ├── routes.py
│   ├── tasks.py
│   ├── cache.py   # Redis caching
│── alembic/
│── docker-compose.yml
│── requirements.txt
│── README.md
```

## CRUD Operations
- **Create Triggers**: Add new triggers with type (scheduled/API) and optional schedule time.
- **Read Events/Triggers**: Fetch all triggers or event logs.
- **Update**: Modify existing triggers.
- **Delete**: Remove old triggers.

## Event Retention
Old events can be retained or archived for efficient storage and quick querying. The `archived` flag is used to distinguish between active and archived events.

## Manual Testing
- **Create Triggers**: Manually add triggers through API endpoints.
- **Trigger Execution**: Test scheduled and API-based triggers manually to verify event handling.

## Running the Project

### Step 1: Start Docker Containers
```sh
docker-compose up --build
```

### Step 2: Run Celery Worker
```sh
celery -A app.tasks worker --loglevel=info
```

### Step 3: Start the FastAPI Server
```sh
uvicorn app.main:app --reload
```

Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Deployment
This project is deployed on **Render**. Access the live application here:

[Event Trigger Platform](https://event-trigger-platform-7svu.onrender.com/docs)

---

## Example API Requests

### 1. Full Payload Example
```json
{
  "name": "Test Trigger - Full Payload",
  "trigger_type": "api",
  "schedule_time": "2025-02-15T17:26:31.342Z",
  "api_payload": {
    "additionalProp1": "value1",
    "additionalProp2": "value2",
    "additionalProp3": "value3"
  }
}
```

### 2. Valid Example with Scheduled Trigger Type
```json
{
  "name": "Scheduled Trigger",
  "trigger_type": "scheduled",
  "schedule_time": "2025-03-01T10:00:00.000Z"
}
```

### 3. Valid Example with Empty Payload
```json
{
  "name": "Empty Payload Trigger",
  "trigger_type": "time-based",
  "schedule_time": "2025-02-15T12:00:00.000Z",
  "api_payload": {}
}
```

### 4. Example with Only Name and Time
```json
{
  "name": "Time Only Example",
  "trigger_type": "time-based",
  "schedule_time": "2025-02-20T08:30:00.000Z"
}
```

### 5. Example with Nested Payload Fields
```json
{
  "name": "Nested Payload Example",
  "trigger_type": "api",
  "api_payload": {
    "config1": "value1",
    "config2": "value2"
  }
}
```

### 6. Invalid Example (Missing trigger_type)
```json
{
  "name": "Missing Trigger Type"
}
```
**Expected Behavior:** API should return an error since `trigger_type` is required.

### 7. Invalid Example (Invalid Trigger Type)
```json
{
  "name": "Invalid Trigger Type Example",
  "trigger_type": "invalid-type"
}
```
**Expected Behavior:** API should return a validation error due to the pattern mismatch.

---

## Production Cost Estimation

For running the system **24x7 for 30 days**, handling **5 queries per day**, the estimated cost breakdown is:

- **Cloud Server (Render/VPS)**: $20 - $40 per month (depending on RAM/CPU requirements)
- **PostgreSQL Database (Managed Service)**: $10 - $30 per month
- **Redis (Managed Service)**: $5 - $15 per month
- **Celery Worker (Compute Cost)**: $10 - $25 per month
- **Miscellaneous (Storage, Logging, Monitoring, etc.)**: $5 - $10 per month

**Total Estimated Monthly Cost:** **$50 - $120**

Feel free to contribute by opening issues or submitting pull requests!

