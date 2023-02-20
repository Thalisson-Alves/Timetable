from dataclasses import dataclass, field

from utils.entities.offer import Offer
from utils.entities.schedule import Schedule


@dataclass
class Discipline:
    id_: str
    name: str
    offers: dict[Schedule, list[Offer]] = field(init=False, default_factory=dict)
    unity: str = ''

    @classmethod
    def with_offers(cls, offers: list[Offer], **kwargs) -> 'Discipline':
        d = cls(**kwargs)
        d.add_offers(offers)
        return d

    @property
    def short_name(self) -> str:
        return ''.join(name[0] for name in self.name.split()
                       if name.isnumeric() or len(name) > 3)

    def add_offer(self, offer: Offer) -> None:
        if not offer.schedule in self.offers:
            self.offers[offer.schedule] = []
        self.offers[offer.schedule].append(offer)

    def add_offers(self, offers: list[Offer]) -> None:
        for offer in offers:
            self.add_offer(offer)

