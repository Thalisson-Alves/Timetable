from typing import Iterable
from dataclasses import dataclass, field

from utils.entities.discipline import Discipline
from utils.entities.offer import Offer


@dataclass(frozen=True)
class Timetable:
    disciplines: Iterable[Discipline]
    offers: Iterable[Offer]
    collisions: list[tuple[Offer, Offer]] = field(init=False, repr=False, default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.collisions

    def __post_init__(self) -> None:
        self._update_collisions()

    def _update_collisions(self) -> None:
        offers_on_day: list[list[Offer]] = [[] for _ in range(7)]
        for offer in self.offers:
            for day in offer.schedule.days:
                self.collisions.extend((offer, o) for o in offers_on_day[day] if offer.collide(o))
                offers_on_day[day].append(offer)

    def __iter__(self):
        return iter(zip(self.disciplines, self.offers))

