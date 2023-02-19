from pytest import fixture

from utils.entities.discipline import Discipline
from utils.entities.offer import Offer
from utils.entities.schedule import Schedule, Time
from utils.entities.timetable import Timetable
from utils.views import markdown_view
from utils.timetable import generate_all_timetables

class TestTimetable:
    @staticmethod
    def test_create_table_with_no_disciplines():
        table = markdown_view.create_table(Timetable([], []))

        assert table == [
            ['   ', 'Segunda', 'Terca', 'Quarta',
             'Quinta', 'Sexta', 'Sabado', 'Domingo'],
            [':---', ':---:', ':---:', ':---:',
             ':---:', ':---:', ':---:', ':---:']
        ]

    @staticmethod
    def test_create_table_with_multiple_disciplines(disciplines_no_collision: list[Discipline]):
        timetables, _ = generate_all_timetables(disciplines_no_collision)
        table = markdown_view.create_table(timetables[0])

        assert table == [
            ['   ', 'Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo'],
            [':---', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:'],
            ['**08:00 as 09:50**', 'D2', 'D2', 'D2', '   ', '   ', '   ', '   '],
            ['**10:00 as 11:50**', 'D1', '   ', 'D1', '   ', 'D1', '   ', '   '],
            ['**14:00 as 15:50**', '   ', 'D3', '   ', 'D3', 'D3', '   ', '   ']
        ]

    @staticmethod
    def test_create_table_with_collision(disciplines_with_collision: list[Discipline]):
        _, timetables = generate_all_timetables(disciplines_with_collision)
        table = markdown_view.create_table(timetables[0])

        assert table == [
            ['   ', 'Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo'],
            [':---', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:'],
            ['**10:00 as 11:50**', 'D1', 'D3', 'D1', 'D3', 'D1~D3', '   ', '   '],
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
                                      arrival=Time.from_string('10:00'),
                                      departure=Time.from_string('11:50')),
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
                                      arrival=Time.from_string('08:00'),
                                      departure=Time.from_string('09:50')),
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
                                      arrival=Time.from_string('14:00'),
                                      departure=Time.from_string('15:50')),
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
                                      arrival=Time.from_string('10:00'),
                                      departure=Time.from_string('11:50')),
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
                                      arrival=Time.from_string('10:00'),
                                      departure=Time.from_string('11:50')),
                )
            ]
        ),
    ]
