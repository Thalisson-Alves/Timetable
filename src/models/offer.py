from dataclasses import dataclass

from models.schedule import Schedule


@dataclass
class Offer:
    code: str
    teacher: str
    schedule: Schedule
    place: str
    vacancy_offered: int
    vacancy_filled: int

    def vacancy_remaining(self) -> int:
        return self.vacancy_offered - self.vacancy_filled

