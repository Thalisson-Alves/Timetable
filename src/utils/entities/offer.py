from dataclasses import dataclass

from utils.entities.schedule import Schedule


@dataclass
class Offer:
    code: str
    teacher: str
    schedule: Schedule
    place: str
    vacancies_offered: int
    vacancies_occuped: int
