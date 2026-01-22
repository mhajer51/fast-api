from abc import ABC, abstractmethod

from app.jobs.base import Job


class Queue(ABC):
    @abstractmethod
    def enqueue(self, job: Job) -> None:
        raise NotImplementedError

    @abstractmethod
    def run_next(self) -> None:
        raise NotImplementedError
