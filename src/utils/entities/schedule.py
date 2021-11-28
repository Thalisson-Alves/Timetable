from dataclasses import dataclass


@dataclass
class Time:
    hour: int
    minutes: int

    @classmethod
    def from_string(cls, content: str):
        hour, minutes = map(int, content.split(':'))
        return cls(hour, minutes)

    def rounded(self) -> 'Time':
        return Time(self.hour + (self.minutes > 0), 0)

    def __lt__(self, other: 'Time') -> bool:
        return float(f'{self.hour}.{self.minutes}') < float(f'{other.hour}.{other.minutes}')

    def __le__(self, other: 'Time') -> bool:
        return float(f'{self.hour}.{self.minutes}') <= float(f'{other.hour}.{other.minutes}')

    def __gt__(self, other: 'Time') -> bool:
        return float(f'{self.hour}.{self.minutes}') > float(f'{other.hour}.{other.minutes}')

    def __ge__(self, other: 'Time') -> bool:
        return float(f'{self.hour}.{self.minutes}') >= float(f'{other.hour}.{other.minutes}')

    def __str__(self) -> str:
        return f'{self.hour:02}:{self.minutes:02}'


@dataclass
class Schedule:
    days: list[int]
    arrival: Time
    departure: Time
