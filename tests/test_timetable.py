from models.discipline import Discipline
from models.timetable import Timetable
from models.schedule import Time, Schedule


class TestTimetable:
    @staticmethod
    def test_no_collisions(disciplines_no_collision: list[Discipline]):
        schedules = [list(d.offers.keys())[0] for d in disciplines_no_collision]

        timetable = Timetable(disciplines_no_collision, schedules)

        assert not timetable.collisions
        assert timetable.is_valid
        assert same_collisions(timetable.collisions, {})

    @staticmethod
    def test_with_1_collision(disciplines_with_1_collision: list[Discipline]):
        schedules = [list(d.offers.keys())[0] for d in disciplines_with_1_collision]
        expected_schedule = Schedule(days=[5],
                                     arrival=Time.from_string('10:00'),
                                     departure=Time.from_string('11:50'))
        expected_collision = {expected_schedule: disciplines_with_1_collision}

        timetable = Timetable(disciplines_with_1_collision, schedules)

        assert not timetable.is_valid
        assert len(timetable.collisions) == 1
        assert len(timetable.collisions[expected_schedule]) == 2
        assert same_collisions(timetable.collisions, expected_collision)

    @staticmethod
    def test_with_2_collisions(disciplines_with_2_collisions: list[Discipline]):
        schedules = [list(d.offers.keys())[0] for d in disciplines_with_2_collisions]
        expected_schedule = [
            Schedule(days=[4],
                     arrival=Time.from_string('10:00'),
                     departure=Time.from_string('11:50')),
            Schedule(days=[5],
                     arrival=Time.from_string('10:00'),
                     departure=Time.from_string('11:50')),
        ]
        expected_collision = {
            expected_schedule[0]: disciplines_with_2_collisions[1:],
            expected_schedule[1]: disciplines_with_2_collisions
        }

        timetable = Timetable(disciplines_with_2_collisions, schedules)

        assert not timetable.is_valid
        assert set(timetable.collisions.keys()) == set(expected_schedule)
        assert same_collisions(timetable.collisions, expected_collision)

    @staticmethod
    def test_with_3_collisions(disciplines_with_3_collisions: list[Discipline]):
        schedules = [list(d.offers.keys())[0] for d in disciplines_with_3_collisions]
        expected_schedule = [
            Schedule(days=[4],
                     arrival=Time.from_string('10:00'),
                     departure=Time.from_string('11:50')),
            Schedule(days=[5],
                     arrival=Time.from_string('10:00'),
                     departure=Time.from_string('11:50')),
            Schedule(days=[3],
                     arrival=Time.from_string('10:00'),
                     departure=Time.from_string('11:50')),
            Schedule(days=[3],
                     arrival=Time.from_string('12:00'),
                     departure=Time.from_string('13:50')),
            Schedule(days=[5],
                     arrival=Time.from_string('12:00'),
                     departure=Time.from_string('13:50')),
        ]
        expected_collision = {
            expected_schedule[0]: disciplines_with_3_collisions[1:3],
            expected_schedule[1]: disciplines_with_3_collisions[:-1],
            expected_schedule[2]: [disciplines_with_3_collisions[i] for i in [0, 3]],
            expected_schedule[3]: disciplines_with_3_collisions[-2:],
            expected_schedule[4]: disciplines_with_3_collisions[-2:],
        }

        timetable = Timetable(disciplines_with_3_collisions, schedules)

        assert not timetable.is_valid
        assert set(timetable.collisions.keys()) == set(expected_schedule)
        assert same_collisions(timetable.collisions, expected_collision)


def same_collisions(actual: dict[Schedule, list[Discipline]], expected: dict[Schedule, list[Discipline]]) -> bool:
    assert actual.keys() == expected.keys()

    for k, v in actual.items():
        assert set(x.id_ for x in v) == set(x.id_ for x in expected[k]), f'On {k}'

    return True

