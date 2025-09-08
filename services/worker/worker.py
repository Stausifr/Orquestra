"""Background worker using RQ."""
from __future__ import annotations

import os
from rq import Queue, Worker
from redis import Redis

from .incident_poller import poll_once
from .discovery_refresher import refresh

redis = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
queue = Queue("orq", connection=redis)


def enqueue_jobs() -> None:
    queue.enqueue(refresh)
    queue.enqueue(poll_once)


def run_worker() -> None:
    Worker([queue], connection=redis).work()


if __name__ == "__main__":
    enqueue_jobs()
    run_worker()
