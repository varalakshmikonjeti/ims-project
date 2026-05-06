# Incident Management System (IMS)

## Overview
This project is a Mission-Critical Incident Management System designed to simulate production-grade monitoring of distributed systems. It ingests signals, creates incidents, manages lifecycle states, and enforces mandatory Root Cause Analysis (RCA) before closure.

---

## Tech Stack
- Backend: FastAPI (Python)
- Frontend: HTML + JavaScript
- Containerization: Docker, Docker Compose
- Storage: In-memory (simulated DB)

---

## Architecture

Frontend → FastAPI Backend → In-Memory Store

### Components:
- Ingestion Layer (/ingest)
- Incident Store (in-memory dictionary)
- State Machine Engine
- RCA Validator
- UI Dashboard

---

## Incident Lifecycle

OPEN → INVESTIGATING → RESOLVED → CLOSED

### Rules:
- RCA is mandatory before CLOSED state
- Invalid transitions are rejected

---

## APIs

### Ingestion
POST /ingest

### Incidents
GET /incidents  
GET /incidents/{id}

### State Update
PUT /incidents/{id}/status

### RCA
POST /incidents/{id}/rca

### Health
GET /health

## Observability
- Health endpoint available at /health for system monitoring
---

## Features

- Async processing using FastAPI BackgroundTasks
- Incident state machine enforcement
- RCA validation before closure
- Real-time dashboard UI
- Dockerized deployment

---

## Design Patterns Used

- State Pattern → Incident lifecycle management
- Strategy Pattern → Alerting logic based on severity
- Producer-Consumer Pattern → Signal ingestion using background processing

---

## Resilience

- Async processing prevents blocking on ingestion
- In-memory store simulates high-speed processing layer
- System designed to handle burst traffic scenarios conceptually

---

## Demo Flow

1. Create Incident using /ingest
2. Move status: OPEN → INVESTIGATING
3. Move status: INVESTIGATING → RESOLVED
4. Submit RCA
5. Move status: CLOSED

---

## How to Run

```bash
docker-compose up --build