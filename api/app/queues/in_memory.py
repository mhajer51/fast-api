from collections import deque

from app.jobs.base import Job
from app.queues.base import Queue


class InMemoryQueue(Queue):
    def __init__(self) -> None:
        self._queue: deque[Job] = deque()

    def enqueue(self, job: Job) -> None:
        self._queue.append(job)

    def run_next(self) -> None:
        if not self._queue:
            return
        job = self._queue.popleft()
        job.run()


default_queue = InMemoryQueue()
