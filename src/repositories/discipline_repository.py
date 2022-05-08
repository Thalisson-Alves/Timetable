from typing import Protocol

from models.discipline import Discipline


class QueryDisciplineRepository(Protocol):
    def get_all(self, filters: dict = None) -> list[Discipline]:
        ...


class PersistentDisciplineRepository(QueryDisciplineRepository):
    def create(self, disciplines: list[Discipline]) -> None:
        ...

    def has_any_entry(self) -> bool:
        ...
