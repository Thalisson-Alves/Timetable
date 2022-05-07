from typing import Protocol

from utils.entities.discipline import Discipline


class Scrapper(Protocol):
    def list_all_disciplines(self,
                             **list_disciplines_kwargs) -> list[Discipline]:
        ...

    def list_disciplines(self, unity: int) -> list[Discipline]:
        ...

    def list_unities(self) -> list[int]:
        ...
