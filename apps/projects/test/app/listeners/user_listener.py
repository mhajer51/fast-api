from app.jobs.send_welcome_email import SendWelcomeEmailJob
from app.queues.in_memory import default_queue


def on_user_created(user) -> None:
    default_queue.enqueue(SendWelcomeEmailJob(email=user.email))
