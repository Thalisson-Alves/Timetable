from pytest import fixture

import main
from models.discipline import Discipline
from models.offer import Offer
from models.schedule import Schedule, Time


class TestTimetable:
    @staticmethod
    def test_create_table_with_no_disciplines():
        table = main.create_table([], [])

        assert table == [
            ['   ', 'Segunda', 'Terca', 'Quarta',
             'Quinta', 'Sexta', 'Sabado', 'Domingo'],
            [':---', ':---:', ':---:', ':---:',
             ':---:', ':---:', ':---:', ':---:']
        ]

    @staticmethod
    def test_create_table_with_multiple_disciplines(disciplines_no_collision: list[Discipline]):
        offers = [discipline.offers[0]
                  for discipline in disciplines_no_collision]

        table = main.create_table(disciplines_no_collision, offers)

        assert table == [
            ['   ', 'Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo'],
            [':---', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:'],
            ['**08:00 as 09:50**', 'D2', 'D2', 'D2', '   ', '   ', '   ', '   '],
            ['**10:00 as 11:50**', 'D1', '   ', 'D1', '   ', 'D1', '   ', '   '],
            ['**14:00 as 15:50**', '   ', 'D3', '   ', 'D3', 'D3', '   ', '   ']
        ]

    @staticmethod
    def test_create_table_with_collision(disciplines_with_collision: list[Discipline]):
        offers = [discipline.offers[0]
                  for discipline in disciplines_with_collision]

        table = main.create_table(disciplines_with_collision, offers)

        assert table == [
            ['   ', 'Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo'],
            [':---', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:'],
            ['**10:00 as 11:50**', 'D1', 'D3', 'D1', 'D3', 'D1|D3', '   ', '   '],
        ]


@fixture
def disciplines_no_collision() -> list[Discipline]:
    return [
        Discipline(
            id_='TEST0001',
            name='Discipline 1',
            offers=[
                Offer(
                    code='A',
                    teacher='Teacher 1',
                    place='REMOTO',
                    vacancies_occupied=0,
                    vacancies_offered=10,
                    schedule=Schedule(days=[1, 3, 5],
                                      arrival=Time(10, 0),
                                      departure=Time(11, 50)),
                )
            ]
        ),
        Discipline(
            id_='TEST0002',
            name='Discipline 2',
            offers=[
                Offer(
                    code='B',
                    teacher='Teacher 2',
                    place='REMOTO',
                    vacancies_occupied=0,
                    vacancies_offered=10,
                    schedule=Schedule(days=[1, 2, 3],
                                      arrival=Time(8, 0),
                                      departure=Time(9, 50)),
                ),
            ]
        ),
        Discipline(
            id_='TEST0003',
            name='Discipline 3',
            offers=[
                Offer(
                    code='A',
                    teacher='Teacher 1',
                    place='REMOTO',
                    vacancies_occupied=0,
                    vacancies_offered=10,
                    schedule=Schedule(days=[2, 4, 5],
                                      arrival=Time(14, 0),
                                      departure=Time(15, 50)),
                )
            ]
        ),
    ]


@fixture
def disciplines_with_collision() -> list[Discipline]:
    return [
        Discipline(
            id_='TEST0001',
            name='Discipline 1',
            offers=[
                Offer(
                    code='A',
                    teacher='Teacher 1',
                    place='REMOTO',
                    vacancies_occupied=0,
                    vacancies_offered=10,
                    schedule=Schedule(days=[1, 3, 5],
                                      arrival=Time(10, 0),
                                      departure=Time(11, 50)),
                )
            ]
        ),
        Discipline(
            id_='TEST0003',
            name='Discipline 3',
            offers=[
                Offer(
                    code='A',
                    teacher='Teacher 1',
                    place='REMOTO',
                    vacancies_occupied=0,
                    vacancies_offered=10,
                    schedule=Schedule(days=[2, 4, 5],
                                      arrival=Time(10, 0),
                                      departure=Time(11, 50)),
                )
            ]
        ),
    ]
