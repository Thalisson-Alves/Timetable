from typing import Protocol

from utils.entities.discipline import Discipline


class Scrapper(Protocol):
    def list_all_disciplines(self,
                             **list_disciplines_kwargs) -> list[Discipline]:
        ...

    def list_disciplines(self, unity: int, year: int = 2022,
                         period: int = 1) -> list[Discipline]:
        ...

    def list_unities(self) -> list[int]:
        ...
