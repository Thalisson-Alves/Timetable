from itertools import product

from models.discipline import Discipline
from models.timetable import Timetable


def generate_all_timetables(disciplines: list[Discipline]) -> list[Timetable]:
    return [
        Timetable(disciplines, offers)
        for offers in product(*(discipline.offers for discipline in disciplines))
    ]

