from itertools import product

from utils.entities.discipline import Discipline
from utils.entities.timetable import Timetable


def generate_all_timetables(disciplines: list[Discipline]) -> tuple[list[Timetable], list[Timetable]]:
    valid, invalid = [], []
    for offers in product(*(discipline.offers for discipline in disciplines)):
        timetable = Timetable(disciplines, offers)
        to_add = valid if timetable.is_valid else invalid
        to_add.append(timetable)
    return valid, invalid
