# Async Task Platform

**Distributed background job system with transactional locking, retries, and fault-tolerant workers built using FastAPI, PostgreSQL, and Docker.**

A distributed, database-backed task execution platform built with FastAPI, PostgreSQL, SQLAlchemy, and Docker — supporting concurrent workers, retries, fault tolerance, and task lifecycle tracking.

This project models how production job queues (e.g., Celery, Temporal, Sidekiq) work internally and is implemented from scratch for learning and production purposes.

---

## Architecture

Client → FastAPI → PostgreSQL ← Worker(s)
                      ↑
                Task Logs

- **FastAPI** exposes the HTTP API for job submission and status checks.
- **PostgreSQL** is the source-of-truth for task state and logs and provides transactional locking for safe worker coordination.
- **Worker(s)** poll the database for pending tasks and execute them concurrently.

---

## Components

- **FastAPI service** — accepts new tasks and exposes task status & results.
- **PostgreSQL** — durable storage for tasks, retries, and logs; supports transactional locking (`SELECT ... FOR UPDATE SKIP LOCKED`).
- **Worker service** — polls for pending tasks, executes jobs, handles retries, and persists logs.
- **Alembic** — manages schema migrations.
- **Docker Compose** — runs the API, worker, and Postgres as isolated containers for easy local development.

---

## Task Lifecycle

Each task moves through the following states:

- **PENDING** → **RUNNING** → **COMPLETED**
                 ↘
                  **FAILED** (after max retries)

Workers acquire jobs using `SELECT ... FOR UPDATE SKIP LOCKED` to ensure:
- No two workers run the same task concurrently
- Horizontal scaling works correctly

---

## Failure & Retry Handling

If a task raises an error, the worker will:
- Log the failure to `task_logs`
- Increment the retry count
- Apply exponential backoff before re-queueing

After `max_retries` is exceeded, the task is marked **FAILED** and all attempts remain persisted for full auditability.

---

## Why This System Is Non-Trivial

This project intentionally avoids managed queues (Redis, Celery, SQS) and implements:

- Distributed locking via PostgreSQL row locks
- Exactly-once task acquisition using `FOR UPDATE SKIP LOCKED`
- Durable retry semantics with exponential backoff
- Persistent execution logs for observability

This is the same class of engineering problem solved by production systems like Celery, Sidekiq, Temporal, and AWS SQS — implemented from first principles.

---

## Scaling Model

The system scales horizontally by adding worker containers:

```bash
docker compose up --scale worker=5
```

Each worker safely competes for jobs using PostgreSQL transactional locking.  
No coordination service or message broker is required.

This allows:
- Linear throughput scaling
- Zero duplicate execution
- Crash-safe job recovery

This makes it clear this is not a single-process toy.

---

## Running Locally

1. Build and start services:

```bash
docker compose up --build
```

2. Run migrations:

```bash
docker compose exec api alembic upgrade head
```

The API will be available at: `http://localhost:8000`

Swagger UI: `http://localhost:8000/docs`

---

## API Usage


### Create a Task

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"payload": {"job": "process data"}}'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "status": "PENDING",
  "payload": { "job": "process data" },
  "retry_count": 0,
  "max_retries": 3,
  "result": null,
  "error": null,
  "created_at": "2026-01-12T10:30:00Z"
}
```

### Check Task Status

```bash
curl http://localhost:8000/tasks/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "status": "COMPLETED",
  "payload": { "job": "process data" },
  "retry_count": 0,
  "max_retries": 3,
  "result": "42",
  "error": null,
  "created_at": "2026-01-12T10:30:00Z"
}
```

### Retrieve Task Logs

```bash
curl http://localhost:8000/tasks/1/logs
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "task_id": 1,
    "message": "Task picked up by worker",
    "created_at": "2026-01-12T10:30:01Z"
  },
  {
    "id": 2,
    "task_id": 1,
    "message": "Task completed successfully",
    "created_at": "2026-01-12T10:30:05Z"
  }
]
```

---

## Notes & Tips

- Use **Docker Compose** for fast local development and to mirror production container behavior.
- If you run multiple worker replicas, they will coordinate safely using PostgreSQL row locking.
- The Swagger UI (`http://localhost:8000/docs`) is useful for interactive API testing.

---

## Development

### Project Structure

```
backend/
├── app/
│   ├── api/           # FastAPI route handlers
│   ├── models/        # SQLAlchemy ORM models
│   ├── workers/       # Worker processes
│   ├── core/          # Config and utilities
│   └── db/            # Database session & migrations
├── alembic/           # Database migrations
└── requirements.txt   # Python dependencies
```

### Database Migrations

Create a new migration:

```bash
docker compose exec api alembic revision --autogenerate -m "description"
```

Apply migrations:

```bash
docker compose exec api alembic upgrade head
```

---

## Contributing

This is a personal project built for learning and demonstration purposes. If you'd like to use or extend this:

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes** and test them locally
4. **Commit your changes**: `git commit -m 'Add feature'`
5. **Push to the branch**: `git push origin feature/your-feature`
6. **Open a pull request** with a clear description

### Code Style

- Format code with **Black** and **isort**
- Follow PEP 8 guidelines
- Write docstrings for all functions and classes

---

## License

This project is provided as-is for educational and portfolio purposes.
