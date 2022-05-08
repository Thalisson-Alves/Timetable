from dataclasses import dataclass


@dataclass
class Time:
    # TODO - maybe refactor that to store only the minutes
    #  and create a prop to the hour
    hour: int
    minutes: int

    @classmethod
    def from_string(cls, content: str):
        hour, minutes = map(int, content.split(':'))
        return cls(hour, minutes)

    @property
    def in_minutes(self) -> int:
        return self.hour * 60 + self.minutes

    def rounded_up(self) -> 'Time':
        return Time(self.hour + (self.minutes > 0), 0)

    def __lt__(self, other: 'Time') -> bool:
        return self.in_minutes < other.in_minutes

    def __le__(self, other: 'Time') -> bool:
        return self.in_minutes <= other.in_minutes

    def __gt__(self, other: 'Time') -> bool:
        return self.in_minutes > other.in_minutes

    def __ge__(self, other: 'Time') -> bool:
        return self.in_minutes >= other.in_minutes

    def __str__(self) -> str:
        return f'{self.hour:02}:{self.minutes:02}'

    def __hash__(self) -> int:
        return hash((self.hour, self.minutes))


@dataclass
class Schedule:
    days: list[int]
    arrival: Time
    departure: Time
