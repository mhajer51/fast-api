from abc import ABC, abstractmethod


class Seeder(ABC):
    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError
