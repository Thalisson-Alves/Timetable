from models.discipline import Discipline
from utils.scrappers.discipline_scrapper import DisciplineScrapper


class ScrapperDisciplineRepository:
    _disciplines: list[Discipline]

    @classmethod
    def init(cls, scrapper: DisciplineScrapper):
        cls._disciplines = scrapper.list_all_disciplines()

    @classmethod
    def get_all(cls, filters: dict = None) -> list[Discipline]:
        return [discipline for discipline in cls._disciplines
                for key, value in filters.items()
                if getattr(discipline, key) == value]
