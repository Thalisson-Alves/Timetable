from dataclasses import dataclass

from utils.entities.schedule import Schedule


@dataclass
class Offer:
    code: str
    teacher: str
    schedule: Schedule
    place: str
    vacancies_offered: int
    vacancies_occupied: int

    def collide(self, other: 'Offer') -> bool:
        return self.schedule.departure > other.schedule.arrival and other.schedule.departure > self.schedule.arrival

