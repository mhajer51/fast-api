from app.events.dispatcher import dispatcher
from app.events.user_events import USER_CREATED
from app.listeners.user_listener import on_user_created


def register_listeners() -> None:
    dispatcher.register(USER_CREATED, on_user_created)
