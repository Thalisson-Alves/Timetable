import argparse

from models.discipline import Discipline
from repositories.scrapper_discipline_repository import ScrapperDisciplineRepository
from scrappers.sigaa_scrapper import SIGAAScrapper
from utils.timetable import generate_all_timetables
from views import markdown_view


def main(args: argparse.Namespace):
    ScrapperDisciplineRepository.init(SIGAAScrapper())

    if args.list:
        display_disciplines()

    if args.disciplines:
        disciplines = [discipline for name in args.disciplines
                       if (discipline := discipline_for_name(name))]
    else:
        disciplines = read_disciplines()

    all_timetables = generate_all_timetables(disciplines)
    markdown_view.save_to_file(args.output_file, all_timetables)


def display_disciplines():
    print('All available disciplines:\n')
    print('-' * 30)
    for discipline in ScrapperDisciplineRepository.get_all():
        print(f'Code: {discipline.id_} \t Name: {discipline.name}')
    print('-' * 30)


def read_disciplines() -> list[Discipline]:
    disciplines = []
    while True:
        discipline_name = input('Discipline name: ')
        if not discipline_name:
            break

        discipline = discipline_for_name(discipline_name)
        if discipline:
            disciplines.append(discipline)
            print('Discipline added')
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

