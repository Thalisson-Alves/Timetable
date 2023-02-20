from dataclasses import dataclass
from typing import Optional


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

    def add_minutes(self, minutes: int) -> 'Time':
        return Time(self.total_minutes + minutes)

    def __str__(self) -> str:
        return f'{self.hours:02}:{self.minutes:02}'


@dataclass
class Schedule:
    days: list[int]
    arrival: Time
    departure: Time

    def intersection(self, other: 'Schedule') -> Optional['Schedule']:
        common_days = set(self.days) & set(other.days)
        if not common_days or self.departure <= other.arrival or other.departure <= self.arrival:
            return None

        return Schedule(
            days=list(common_days),
            arrival=Time(max(self.arrival.total_minutes, other.arrival.total_minutes)),
            departure=Time(min(self.departure.total_minutes, other.departure.total_minutes))
        )

    def __hash__(self) -> int:
        return hash((tuple(self.days), self.arrival, self.departure))

