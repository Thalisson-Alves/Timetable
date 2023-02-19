from dataclasses import dataclass


@dataclass(order=True, unsafe_hash=True)
class Time:
    total_minutes: int

    @property
    def hours(self) -> int:
        return self.total_minutes // 60

    @property
    def minutes(self) -> int:
        return self.total_minutes % 60

    @classmethod
    def from_string(cls, content: str):
        hours, minutes = map(int, content.split(':'))
        return cls(hours * 60 + minutes)

    def rounded_up(self) -> 'Time':
        hours, minutes = divmod(self.total_minutes, 60)
        return Time((hours + (minutes > 0)) * 60)

    def __str__(self) -> str:
        return f'{self.hours:02}:{self.minutes:02}'


@dataclass
class Schedule:
    days: list[int]
    arrival: Time
    departure: Time

