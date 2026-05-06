from datetime import datetime
from store import INCIDENTS

ALLOWED_TRANSITIONS = {
    "OPEN": ["INVESTIGATING"],
    "INVESTIGATING": ["RESOLVED"],
    "RESOLVED": ["CLOSED"]
}

def calculate_mttr(incident):
    if incident.get("resolved_at"):
        return (incident["resolved_at"] - incident["created_at"]).total_seconds()
    return None


def can_transition(current, new):
    return new in ALLOWED_TRANSITIONS.get(current, [])


def validate_close(incident):
    if not incident.get("rca"):
        return False, "RCA required before closing"
    return True, None