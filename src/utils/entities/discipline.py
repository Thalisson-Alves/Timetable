from dataclasses import dataclass, field

from utils.entities.offer import Offer


@dataclass
class Discipline:
    id_: str
    name: str
    offers: list[Offer] = field(default_factory=list)

    @property
    def short_name(self) -> str:
        return ''.join(name[0] for name in self.name.split() if name.isnumeric() or len(name) > 3)
