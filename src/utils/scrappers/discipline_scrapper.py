from typing import Protocol

from models.discipline import Discipline


class DisciplineScrapper(Protocol):
    def list_all_disciplines(self) -> list[Discipline]:
        ...

    def list_disciplines(self, unity: int) -> list[Discipline]:
        ...

    def list_unities(self) -> list[int]:
        ...
