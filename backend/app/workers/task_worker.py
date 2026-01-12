import time
import traceback
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.task import Task, TaskStatus
from app.models.task_log import TaskLog

POLL_INTERVAL_SECONDS = 2


def log(db: Session, task_id: int, message: str):
    db.add(TaskLog(task_id=task_id, message=message))
    db.commit()


def process_task(db: Session, task: Task):
    try:
        log(db, task.id, "Task picked up by worker")

        task.status = TaskStatus.RUNNING
        db.commit()
        log(db, task.id, "Task running")

        # ---- Simulated work ----
        time.sleep(5)

        if task.payload.get("fail"):
            raise RuntimeError("Simulated failure")

        result = {"message": "task completed successfully"}
        # ------------------------

        task.status = TaskStatus.COMPLETED
        task.result = result
        db.commit()
        log(db, task.id, "Task completed successfully")

        return   # 🚨 CRITICAL: stop here, never retry on success

    except Exception:
        db.rollback()

        task.retry_count += 1
        task.error = traceback.format_exc()

        if task.retry_count >= task.max_retries:
            task.status = TaskStatus.FAILED
            db.commit()
            log(db, task.id, "Task permanently failed")
        else:
            task.status = TaskStatus.PENDING
            db.commit()
            log(db, task.id, f"Retrying task ({task.retry_count}/{task.max_retries})")

        time.sleep(2 ** task.retry_count)


def run_worker():
    print("Worker started. Polling for tasks...")

    while True:
        db = SessionLocal()
        try:
            task = (
                db.query(Task)
                .filter(Task.status == TaskStatus.PENDING)
                .order_by(Task.created_at)
                .with_for_update(skip_locked=True)
                .first()
            )

            if not task:
                time.sleep(POLL_INTERVAL_SECONDS)
                continue

            print(f"Picked task {task.id}")
            process_task(db, task)

        finally:
            db.close()


if __name__ == "__main__":
    run_worker()
