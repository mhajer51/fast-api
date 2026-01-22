from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventDispatcher:
    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[..., None]]] = defaultdict(list)

    def register(self, event_name: str, listener: Callable[..., None]) -> None:
        self._listeners[event_name].append(listener)

    def dispatch(self, event_name: str, **payload: Any) -> None:
        for listener in self._listeners.get(event_name, []):
            listener(**payload)


dispatcher = EventDispatcher()
