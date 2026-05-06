from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from datetime import datetime
from collections import defaultdict
import uuid
import time

signal_buffer = defaultdict(list)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

incidents: Dict[str, dict] = {}

# STATE MACHINE
ALLOWED_TRANSITIONS = {
    "OPEN": ["INVESTIGATING"],
    "INVESTIGATING": ["RESOLVED"],
    "RESOLVED": ["CLOSED"]
}

class SignalIn(BaseModel):
    component_id: str
    severity: str

class RCA(BaseModel):
    root_cause: str
    fix: str
    prevention: str

class StatusUpdate(BaseModel):
    status: str


def process_signal(signal: SignalIn):
    print(f"[BG] Processing {signal.component_id}")


@app.get("/")
def root():
    return {"message": "IMS Running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# CREATE INCIDENT
@app.post("/ingest")
async def ingest(signal: SignalIn, bg: BackgroundTasks):
    bg.add_task(process_signal, signal)

    incident_id = str(uuid.uuid4())

    incidents[incident_id] = {
        "id": incident_id,
        "component_id": signal.component_id,
        "severity": signal.severity,
        "status": "OPEN",
        "created_at": datetime.utcnow(),
        "resolved_at": None,
        "rca": None
    }

    return {"status": "created", "incident_id": incident_id}


# GET ALL
@app.get("/incidents")
def get_incidents():
    return list(incidents.values())


# GET ONE
@app.get("/incidents/{incident_id}")
def get_incident(incident_id: str):
    if incident_id not in incidents:
        raise HTTPException(status_code=404)
    return incidents[incident_id]


# STATUS UPDATE (STATE MACHINE ADDED)
@app.put("/incidents/{incident_id}/status")
def update_status(incident_id: str, data: StatusUpdate):

    if incident_id not in incidents:
        raise HTTPException(status_code=404)

    incident = incidents[incident_id]
    current = incident["status"]
    new = data.status

    # ❌ invalid transition check
    if new not in ALLOWED_TRANSITIONS.get(current, []):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transition {current} → {new}"
        )

    # ❌ RCA check before closing
    if new == "CLOSED":
        if not incident["rca"]:
            raise HTTPException(status_code=400, detail="RCA required before closing")
        incident["resolved_at"] = datetime.utcnow()

    incident["status"] = new
    return {"message": "status updated"}


# RCA + MTTR LOGIC
@app.post("/incidents/{incident_id}/rca")
def add_rca(incident_id: str, rca: RCA):

    if incident_id not in incidents:
        raise HTTPException(status_code=404)

    incident = incidents[incident_id]

    incident["rca"] = rca.dict()
    incident["status"] = "RESOLVED"
    incident["resolved_at"] = datetime.utcnow()

    # MTTR calculation
    mttr = (incident["resolved_at"] - incident["created_at"]).total_seconds()
    incident["mttr"] = mttr

    return {
        "message": "RCA added",
        "mttr_seconds": mttr
    }