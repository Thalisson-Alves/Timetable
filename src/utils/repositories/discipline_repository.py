from utils.entities.discipline import Discipline
from utils.entities.offer import Offer
from utils.repositories.web_scraping import load_disciplines


class DisciplineRepository:
    _disciplines: list[Discipline] = load_disciplines()

    @classmethod
    def get(cls, discpline_id: str) -> Discipline | None:
        for discipline in cls._disciplines:
            if discipline.id_ == discpline_id:
                return discipline

    @classmethod
    def get_by_offer(cls, offer: Offer) -> list[Discipline]:
        return [discipline for discipline in cls._disciplines
                if offer in discipline]

    @classmethod
    def get_by_names(cls, names: list[str]) -> list[Discipline]:
        return [discipline for discipline in cls._disciplines
                if any(name.lower() in discipline.name.lower()
                       for name in names)]

    @classmethod
    def get_by_name(cls, name: str) -> list[Discipline]:
        return [discipline for discipline in cls._disciplines
                if name.lower() in discipline.name.lower()]
