from datetime import datetime

INCIDENTS = {}
SIGNALS = {}

def now():
    return datetime.utcnow()