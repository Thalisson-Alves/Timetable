import unicodedata
import io

from utils.entities.timetable import Timetable


def save_to_file(file_name: str, valid: list[Timetable], invalid: list[Timetable]):
    with open(file_name, 'w') as file:
        file.write('# Timetables\n\n## Valid\n\n')
        save_timetables(file, valid)
        file.write('## Invalid\n\n')
        save_timetables(file, invalid)

    print(f'\nSaved result on file: {file_name}')


def save_timetables(file: io.TextIOBase, timetables: list[Timetable]) -> None:
    for i, timetable in enumerate(timetables, 1):
        table = create_table(timetable)

        file.write(f'### Grade {i:02}\n\n')
        file.writelines(('|' + '|'.join(row) + '|\n' for row in table))
        file.write(generate_legend(timetable))


def generate_legend(timetable: Timetable) -> str:
    legend = '\n<details>\n<summary>Legenda das ofertas</summary>\n\n'
    for discipline, offer in timetable:
        legend += f'- {discipline.short_name}: {discipline.name}\n'
        legend += f'  - Turma: {offer.code}\n'
        legend += f'  - Professor(a): {offer.teacher}\n'
        legend += f'  - Local: {offer.place}\n'
        legend += f'  - Vagas restantes: {offer.vacancies_offered - offer.vacancies_occupied}\n'

    return ''.join(char for char in unicodedata.normalize('NFD', legend)
                   if unicodedata.category(char) != 'Mn') + '</details>\n\n'


def create_table(timetable: Timetable) -> list[list[str]]:
    header = ['Segunda', 'Terca', 'Quarta',
              'Quinta', 'Sexta', 'Sabado', 'Domingo']
    separator = [':---:'] * len(header)

    schedules = sorted({(offer.schedule.arrival, offer.schedule.departure)
                           for offer in timetable.offers})

    body = [['   '] * len(header) for _ in range(len(schedules))]
    for discipline, offer in timetable:
        for day in offer.schedule.days:
            for i, (start, end) in enumerate(schedules):
                if offer.schedule.departure > start and end > offer.schedule.arrival:
                    current_cell = body[i][(day - 1) % len(header)].strip()
                    cell_name = discipline.short_name if not current_cell else f'{current_cell}~{discipline.short_name}'
                    body[i][(day - 1) % len(header)] = cell_name

    for i, (arrival, departure) in enumerate(schedules[1:], 1):
        schedules[i] = (max(arrival, schedules[i-1][1].rounded_up()), departure)

    first_column = [f'**{arrival} as {departure}**'
                    for arrival, departure in schedules]
    return [[row_info, *row] for row_info, row
            in zip(['   ', ':---', *first_column],
                   [header, separator, *body])]

