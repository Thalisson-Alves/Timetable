from typing import Sequence, Iterator
from dataclasses import dataclass, field

from models.discipline import Discipline
from models.schedule import Schedule


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
        schedules_per_day: list[list[tuple[Schedule, int]]] = [[] for _ in range(7)]
        for i, schedule in enumerate(self.schedules):
            for day in schedule.days:
                one_day_schedule = Schedule(days=[day],
                                            arrival=schedule.arrival,
                                            departure=schedule.departure)
                schedules_per_day[day].append((one_day_schedule, i))

        for schedules in schedules_per_day:
            if not schedules:
                continue

            schedules.sort()

            current, ci = schedules[0]
            for next, ni in schedules[1:]:
                intersection = current.intersection(next)
                if not intersection:
                    current = next
                    continue

                if intersection not in self.collisions:
                    self.collisions[intersection] = [self.disciplines[ni], self.disciplines[ci]]
                else:
                    self.collisions[intersection].append(self.disciplines[ni])

                current = current.surplus(next)
                if not current:
                    current = next

    def __iter__(self) -> Iterator[tuple[Discipline, Schedule]]:
        yield from ((d, s) for d, s in zip(self.disciplines, self.schedules))

