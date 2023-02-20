import io
import unicodedata

from utils.entities.discipline import Discipline
from utils.entities.timetable import Timetable
from utils.timetable import generate_all_timetables, remove_duplicates_sorted_seq


def save_to_file(file_name: str, disciplines: list[Discipline]) -> None:
    valid, invalid = generate_all_timetables(disciplines)
    with open(file_name, 'w') as file:
        file.write('# Timetables\n\n## Valid\n\n')
        save_timetables(file, valid)
        file.write('## Invalid\n\n')
        save_timetables(file, sorted(invalid, key=lambda x: len(x.collisions)))

    print(f'\nSaved result on file: {file_name}')


def save_timetables(file: io.TextIOBase, timetables: list[Timetable]) -> None:
    for i, timetable in enumerate(timetables, 1):
        table = create_table(timetable)

        file.write(f'### Grade {i:02}\n\n')
        file.writelines(('|' + '|'.join(row) + '|\n' for row in table))
        file.write(generate_legend(timetable))


def generate_legend(timetable: Timetable) -> str:
    legend = '\n<details>\n<summary>Legenda das ofertas</summary>\n\n'
    for discipline, schedule in timetable:
        offers = discipline.offers[schedule]

        legend += f'- {discipline.short_name}: {discipline.name}\n'
        legend += f'  - Turma: {",".join(o.code for o in offers)}\n'
        legend += f'  - Professor(a): {",".join(o.teacher for o in offers)}\n'
        legend += f'  - Local: {",".join(o.place for o in offers)}\n'
        legend += f'  - Vagas restantes: {",".join(str(o.vacancy_remaining()) for o in offers)}\n'

    return ''.join(char for char in unicodedata.normalize('NFD', legend)
                   if unicodedata.category(char) != 'Mn') + '</details>\n\n'


def create_table(timetable: Timetable) -> list[list[str]]:
    header = ['Segunda', 'Terca', 'Quarta',
              'Quinta', 'Sexta', 'Sabado', 'Domingo']
    separator = [':---:'] * len(header)

    schedules = sorted((schedule.arrival, schedule.departure)
                       for schedule in timetable.schedules)

    for i, (arrival, departure) in enumerate(schedules):
        start = arrival
        end = departure
        if i < len(schedules) - 1:
            end = min(departure, schedules[i+1][schedules[i+1][0] == arrival].rounded_up().add_minutes(-10))
        schedules[i] = (start, end)

    schedules = remove_duplicates_sorted_seq(schedules)

    body = [['   '] * len(header) for _ in range(len(schedules))]
    for discipline, schedule in timetable:
        for day in schedule.days:
            for i, (start, end) in enumerate(schedules):
                if schedule.departure > start and end > schedule.arrival:
                    current_cell = body[i][(day - 1) % len(header)].strip()
                    cell_name = discipline.short_name if not current_cell else f'{current_cell}~{discipline.short_name}'
                    body[i][(day - 1) % len(header)] = cell_name

    first_column = [f'**{arrival} as {departure}**'
                    for arrival, departure in schedules]
    return [[row_info, *row] for row_info, row
            in zip(['   ', ':---', *first_column],
                   [header, separator, *body])]

