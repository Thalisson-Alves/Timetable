from typing import Sequence, Iterator
from dataclasses import dataclass, field

from utils.entities.discipline import Discipline
from utils.entities.schedule import Schedule


@dataclass(frozen=True)
class Timetable:
    disciplines: Sequence[Discipline]
    schedules: Sequence[Schedule]
    collisions: dict[Schedule, list[Discipline]] = field(init=False, repr=False, default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return not self.collisions

    def __post_init__(self) -> None:
        self._update_collisions()

    def _update_collisions(self) -> None:
        # TODO: Fix this collision check or remove completly
        for i, s1 in enumerate(self.schedules):
            for j, s2 in enumerate(self.schedules[i+1:]):
                intersection = s1.intersection(s2)
                if not intersection:
                    continue
                if intersection not in self.collisions:
                    self.collisions[intersection] = []
                self.collisions[intersection].append(self.disciplines[i])

    def __iter__(self) -> Iterator[tuple[Discipline, Schedule]]:
        yield from ((d, s) for d, s in zip(self.disciplines, self.schedules))

