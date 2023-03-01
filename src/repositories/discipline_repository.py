from typing import Protocol

from models.discipline import Discipline


class DisciplineRepository(Protocol):
    def get(self, discipline_id: str) -> Discipline | None:
        ...

    def get_all(self, length: int | None = None,
                offset: int | None = None) -> list[Discipline]:
        ...

    def get_by_names(self, names: list[str]) -> list[Discipline]:
        ...

    def get_by_name(self, name: str) -> list[Discipline]:
        ...

