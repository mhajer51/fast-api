from dataclasses import dataclass

from app.jobs.base import Job


@dataclass
class SendWelcomeEmailJob(Job):
    email: str

    def run(self) -> None:
        # Placeholder for actual email integration.
        return None
