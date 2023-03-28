import argparse

from models.discipline import Discipline
from repositories.scrapper_discipline_repository import ScrapperDisciplineRepository
from scrappers.sigaa_scrapper import SIGAAScrapper
from utils.timetable import generate_all_timetables
from views import markdown_view


def main(args: argparse.Namespace):
    ScrapperDisciplineRepository.init(SIGAAScrapper())

    # TODO - Factor this ??
    #      - I guess it would be better if this kind of thing
    #        was a subcommand instead of an argument
    if args.watch:
        discipline = discipline_for_name(args.watch)
        if not discipline:
            print('Discipline not found. Try again.')
            return

        watch_discipline(discipline.id_)
        return

    if args.list:
        display_disciplines()

    if args.disciplines:
        disciplines = [discipline for name in args.disciplines
                       if (discipline := discipline_for_name(name))]
    else:
        disciplines = read_disciplines()

    all_timetables = generate_all_timetables(disciplines)
    markdown_view.save_to_file(args.output_file, all_timetables)


def watch_discipline(discipline_id: str):
    import os
    from time import sleep

    counter = 0
    while True:
        try:
            sleep(30)
            counter += 1

            ScrapperDisciplineRepository.init(SIGAAScrapper())

            discipline = ScrapperDisciplineRepository.get(discipline_id)
            if not discipline:
                continue

            remaining = 0
            for offers in discipline.offers.values():
                remaining = sum(o.vacancy_remaining for o in offers)

            print(f'\r{counter} - There are {remaining} remaining vacancies on {discipline.name}', end='', flush=True)
            if remaining:
                # TODO - Use a better notifier, maybe send an e-mail or something
                os.system(f'spd-say "Hurry up! Only {remaining} vacancy in {discipline.name}"')
                print()
        except KeyboardInterrupt: break
        except: ...


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
            print(f'Discipline {discipline.name} added')
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
    # TODO - Add argument to configure the time between requests
    #      - Add argument to specify which offer to scrap (based on schedule, teacher, ...)
    parser.add_argument('-w', '--watch', type=str, default='',
                        help='Discipline to watch for vacancies')
    return parser.parse_args()


if __name__ == '__main__':
    main(parsed_args())

