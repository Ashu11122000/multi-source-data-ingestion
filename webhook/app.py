
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone


app = FastAPI(
    title="Mock Webhook Ingestion Service",
    description="Simulates push-based event ingestion",
    version="1.0.0"
)


# Define incoming event structure
class CustomerEvent(BaseModel):
    customer_id: str
    full_name: str
    email: str
    city: str
    created_at: str


# Store incoming events temporarily
received_events = []


@app.get("/")
def home():
    return {
        "message": "Webhook ingestion service is running"
    }


@app.post("/webhook/customers")
def receive_customer_event(event: CustomerEvent):

    event_data = event.model_dump()

    event_data["source"] = "webhook"
    event_data["ingested_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    received_events.append(event_data)

    return {
        "status": "success",
        "message": "Customer event received",
        "total_events": len(received_events),
        "data": event_data
    }


@app.get("/webhook/events")
def get_received_events():

    return {
        "total_events": len(received_events),
        "events": received_events
    }
