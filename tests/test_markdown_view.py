from utils.entities.discipline import Discipline
from utils.entities.timetable import Timetable
from utils.views import markdown_view
from utils.timetable import generate_all_timetables

class TestMarkdownView:
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
    def test_create_table_with_1_collision(disciplines_with_1_collision: list[Discipline]):
        _, timetables = generate_all_timetables(disciplines_with_1_collision)
        table = markdown_view.create_table(timetables[0])

        assert table == [
            ['   ', 'Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo'],
            [':---', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:'],
            ['**10:00 as 11:50**', 'D4', 'D5', 'D4', 'D5', 'D4~D5', '   ', '   '],
        ]

    @staticmethod
    def test_create_table_with_2_collisions(disciplines_with_2_collisions: list[Discipline]):
        _, timetables = generate_all_timetables(disciplines_with_2_collisions)
        table = markdown_view.create_table(timetables[0])

        assert table == [
            ['   ', 'Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo'],
            [':---', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:'],
            ['**08:00 as 09:50**', '   ', '   ', '   ', 'D6', 'D6', '   ', '   '],
            ['**10:00 as 11:50**', 'D4', 'D5', 'D4', 'D5~D6', 'D4~D5~D6', '   ', '   '],
        ]

    @staticmethod
    def test_create_table_with_3_collisions(disciplines_with_3_collisions: list[Discipline]):
        _, timetables = generate_all_timetables(disciplines_with_3_collisions)
        table = markdown_view.create_table(timetables[0])

        assert table == [
            ['   ', 'Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo'],
            [':---', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:', ':---:'],
            ['**08:00 as 09:50**', '   ', '   ', '   ', 'D6', 'D6', '   ', '   '],
            ['**10:00 as 11:50**', 'D4', 'D5', 'D4~D7', 'D5~D6', 'D4~D5~D6~D7', '   ', '   '],
            ['**12:00 as 13:50**', '   ', '   ', 'D7~D8', '   ', 'D7~D8', '   ', '   '],
        ]

