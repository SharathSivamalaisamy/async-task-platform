# Async Task Platform

A distributed asynchronous job execution system built with FastAPI, PostgreSQL, Alembic, and Docker.

## Architecture

Client → API → Postgres → Worker

All task state, retries, and logs are stored durably in the database.

## Features
- Asynchronous task execution
- Durable task storage
- Worker locking via SELECT FOR UPDATE SKIP LOCKED
- Retry + failure handling
- Per-task logs
- REST API for submission and polling

## Endpoints

POST /tasks  
GET /tasks/{id}  
GET /tasks/{id}/logs  

## Example

curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"job":"test"}'

curl http://localhost:8000/tasks/1
curl http://localhost:8000/tasks/1/logs
