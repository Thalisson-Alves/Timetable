from pytest import fixture

from utils.entities.discipline import Discipline
from utils.entities.offer import Offer
from utils.entities.schedule import Schedule, Time


next_id_to_use = 1
def create_discipline(*schedules: Schedule):
    global next_id_to_use

    id_ = next_id_to_use
    next_id_to_use += 1
    return Discipline.with_offers(
        id_=f'D{id_}',
        name=f'Discipline {id_}',
        offers=[
            Offer(
                code='A',
                teacher='Teacher 1',
                place='Room 1',
                vacancy_filled=0,
                vacancy_offered=10,
                schedule=schedule
            )
            for schedule in schedules
        ]
    )


@fixture(scope='session')
def disciplines_no_collision() -> list[Discipline]:
    return [
        create_discipline(Schedule(days=[1, 3, 5],
                                   arrival=Time.from_string('10:00'),
                                   departure=Time.from_string('11:50'))),
        create_discipline(Schedule(days=[1, 2, 3],
                                   arrival=Time.from_string('08:00'),
                                   departure=Time.from_string('09:50'))),
        create_discipline(Schedule(days=[2, 4, 5],
                                   arrival=Time.from_string('14:00'),
                                   departure=Time.from_string('15:50'))),
    ]


@fixture(scope='session')
def disciplines_with_1_collision() -> list[Discipline]:
    return [
        create_discipline(Schedule(days=[1, 3, 5],
                                   arrival=Time.from_string('10:00'),
                                   departure=Time.from_string('11:50'))),
        create_discipline(Schedule(days=[2, 4, 5],
                                   arrival=Time.from_string('10:00'),
                                   departure=Time.from_string('11:50'))),
    ]


@fixture(scope='session')
def disciplines_with_2_collisions(disciplines_with_1_collision: list[Discipline]) -> list[Discipline]:
    return [
        *disciplines_with_1_collision,
        create_discipline(Schedule(days=[4, 5],
                                   arrival=Time.from_string('08:00'),
                                   departure=Time.from_string('11:50'))),
    ]

@fixture(scope='session')
def disciplines_with_3_collisions(disciplines_with_2_collisions: list[Discipline]) -> list[Discipline]:
    return [
        *disciplines_with_2_collisions,
        create_discipline(Schedule(days=[3, 5],
                                   arrival=Time.from_string('10:00'),
                                   departure=Time.from_string('13:50'))),
        create_discipline(Schedule(days=[3, 5],
                                   arrival=Time.from_string('12:00'),
                                   departure=Time.from_string('13:50'))),
    ]

