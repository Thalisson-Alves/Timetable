from models.discipline import Discipline
from scrappers.scrapper import Scrapper


class ScrapperDisciplineRepository:
    _disciplines: list[Discipline]

    @classmethod
    def init(cls, scrapper: Scrapper):
        cls._disciplines = scrapper.list_all_disciplines()

    @classmethod
    def get(cls, discipline_id: str) -> Discipline | None:
        for discipline in cls._disciplines:
            if discipline.id_ == discipline_id:
                return discipline

    @classmethod
    def get_all(cls, length: int | None = None, offset: int | None = None) -> list[Discipline]:
        return cls._disciplines[offset:length]

    @classmethod
    def get_by_names(cls, names: list[str]) -> list[Discipline]:
        return [discipline for discipline in cls._disciplines
                if any(name.lower() in discipline.name.lower()
                       for name in names)]

    @classmethod
    def get_by_name(cls, name: str) -> list[Discipline]:
        return [discipline for discipline in cls._disciplines
                if name.lower() in discipline.name.lower()]

