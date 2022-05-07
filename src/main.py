import argparse
from itertools import product
import unicodedata

from utils.entities.discipline import Discipline
from utils.entities.offer import Offer
from utils.repositories.scrapper_discipline_repository import ScrapperDisciplineRepository
from utils.scrappers.sigaa_scrapper import SIGAAScrapper


def main(args: argparse.Namespace):
    # TODO - Save all disciplines on a database,
    #  so we don't need to WebScrap everything again
    ScrapperDisciplineRepository.init(SIGAAScrapper())

    if args.list:
        display_disciplines()

    if args.disciplines:
        disciplines = [discipline for name in args.disciplines
                       if (discipline := discipline_for_name(name))]
    else:
        disciplines = read_disciplines()

    valid_timetables = generate_valid_timetables(disciplines)
    save_to_file(args.output_file, disciplines, valid_timetables)


def display_disciplines():
    print('All available disciplines:\n')
    print('-' * 30)
    for discipline in ScrapperDisciplineRepository.get_all():
        print(f'Code: {discipline.id_} \t Name: {discipline.name}')
    print('-' * 30)


def save_to_file(file_name: str, disciplines: list[Discipline], timetables: list[list[Offer]]) -> None:
    with open(file_name, 'w') as file:
        for i, timetable in enumerate(timetables, 1):
            table = create_table(disciplines, timetable)

            file.write(f'# Grade {i:02}\n\n')
            file.writelines(('|' + '|'.join(row) + '|\n' for row in table))
            file.write(generate_legend(disciplines, timetable))

    print(f'\nSaved result on file: {file_name}')


# TODO - This should be in some sort of MarkDownView class
def generate_legend(disciplines: list[Discipline], timetable: list[Offer]) -> str:
    legend = '\n<details>\n<summary>Legenda das ofertas</summary>\n\n'
    for discipline, offer in zip(disciplines, timetable):
        legend += f'- {discipline.short_name}: {discipline.name}\n'
        legend += f'  - Turma: {offer.code}\n'
        legend += f'  - Professor(a): {offer.teacher}\n'
        legend += f'  - Local: {offer.place}\n'
        legend += f'  - Vagas restantes: {offer.vacancies_offered - offer.vacancies_occupied}\n'

    return ''.join(char for char in unicodedata.normalize('NFD', legend)
                   if unicodedata.category(char) != 'Mn') + '</details>\n\n'


def create_table(disciplines: list[Discipline], timetable: list[Offer]) -> list[list[str]]:
    header = ['Segunda', 'Terca', 'Quarta',
              'Quinta', 'Sexta', 'Sabado', 'Domingo']
    separator = [':---:'] * len(header)

    first_column = sorted({(offer.schedule.arrival, offer.schedule.departure)
                           for offer in timetable})

    body = [['   '] * len(header) for _ in range(len(first_column))]
    for discipline, offer in zip(disciplines, timetable):
        for day in offer.schedule.days:
            for i, (start, end) in enumerate(first_column):
                if offer.schedule.departure > start and end > offer.schedule.arrival:
                    current_cell = body[i][(day - 1) % len(header)].strip()
                    cell_name = discipline.short_name if not current_cell else f'{current_cell}|{discipline.short_name}'
                    body[i][(day - 1) % len(header)] = cell_name

    for i, (arrival, departure) in enumerate(first_column[1:], 1):
        first_column[i] = (max(arrival, first_column[i-1][1].rounded()),
                           departure)

    first_column[:] = [f'**{arrival} as {departure}**'
                       for arrival, departure in first_column]
    return [[row_info, *row] for row_info, row
            in zip(['   ', ':---', *first_column],
                   [header, separator, *body])]


def generate_valid_timetables(disciplines: list[Discipline]) -> list[list[Offer]]:
    return [timetable for timetable in product(*(discipline.offers for discipline in disciplines))
            if is_valid_timetable(timetable)]


def is_valid_timetable(timetable: list[Offer]) -> bool:
    offers_on_day: list[list[Offer]] = [[] for _ in range(7)]
    for offer in timetable:
        for day in offer.schedule.days:
            offers_on_day[day].append(offer)

    for offers in offers_on_day:
        for offer_a in offers:
            for offer_b in offers:
                # Don't compare the same offer with itself
                if offer_a == offer_b:
                    continue

                schedule_a = offer_a.schedule
                schedule_b = offer_b.schedule
                # Check for time collision
                if schedule_b.departure > schedule_a.arrival and schedule_a.departure > schedule_b.arrival:
                    return False

    return True


def read_disciplines() -> list[Discipline]:
    disciplines = []
    while True:
        discipline_name = input('Discipline name: ')
        if not discipline_name:
            break

        discipline = discipline_for_name(discipline_name)
        if discipline:
            disciplines.append(discipline)
        else:
            print('Discipline not found. Try again')
        print()

    return disciplines


def discipline_for_name(discipline_name: str) -> Discipline | None:
    disciplines = ScrapperDisciplineRepository.get_by_name(discipline_name)
    if len(disciplines) == 1:
        return disciplines[0]
    elif len(disciplines) > 1:
        print(f'Which {discipline_name!r}?')
        for index, discipline in enumerate(disciplines):
            print(f'[{index}] - Code: {discipline.id_}, Name: {discipline.name}')
        try:
            discipline_idx = int(input('Indeed Discipline Index: '))
            return disciplines[discipline_idx]
        except (ValueError, IndexError):
            pass
    print(f'\nDiscipline {discipline_name!r} not found!!\n')


def parsed_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Finds all the possible timetables for given disciplines'
    )
    parser.add_argument('-d', '--disciplines', type=str, nargs='+',
                        default=[], required=False,
                        help='Discipline names or codes')
    parser.add_argument('-o', '--output-file', type=str,
                        default='timetables.md',
                        help='Output MarkDown file path')
    parser.add_argument('-l', '--list', action='store_true',
                        help='Display all disciplines')
    return parser.parse_args()


if __name__ == '__main__':
    main(parsed_args())
