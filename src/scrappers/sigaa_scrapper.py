import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from requests.cookies import RequestsCookieJar

from models.discipline import Discipline
from models.offer import Offer
from models.schedule import Schedule, Time

CURRENT_YEAR = int(os.getenv('CURRENT_YEAR', datetime.utcnow().year))
CURRENT_PERIOD = int(os.getenv('CURRENT_PERIOD', (datetime.utcnow().month >= 6) + 1))
# By default Scrap only Faculdade do Gama (673)
POSSIBLE_UNITIES = list(map(int, os.getenv('POSSIBLE_UNITIES', '673').split(',')))
HTML_PATH = os.getenv('HTML_PATH', os.path.join(os.path.dirname(__file__), 'htmls'))


class SIGAAScrapper:
    _url = 'https://sigaa.unb.br/sigaa/public/turmas/listar.jsf'
    _cookies: RequestsCookieJar | None = None

    @classmethod
    def list_all_disciplines(cls):
        return [discipline for unity in cls.list_unities() for discipline in
                cls.list_disciplines(unity)]

    @classmethod
    def list_disciplines(cls, unity: int):
        soup = cls.__create_soup_for(unity, CURRENT_YEAR, CURRENT_PERIOD)
        return cls.__list_disciplines_by_soup(soup)

    @classmethod
    def __create_soup_for(cls, unity: int, year: int,
                          period: int, level: str = 'G') -> BeautifulSoup:
        html = cls.__get_html_from_file(unity=unity, year=year, period=period, level=level)
        if not html:
            html = cls.__get_html_website(unity=unity, year=year, period=period, level=level)
            with open(get_html_filename(unity=unity, year=year, period=period, level=level), 'w', encoding='utf-8') as f:
                f.write(html)

        return BeautifulSoup(html, 'html.parser')

    @classmethod
    def __get_html_from_file(cls, unity: int, year: int,
                             period: int, level: str) -> str:
        try:
            with open(get_html_filename(unity=unity, year=year, period=period, level=level), 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return ''

    @classmethod
    def __get_html_website(cls, unity: int, year: int,
                          period: int, level: str) -> str:
        if not cls._cookies:
            cls._cookies = requests.get(cls._url).cookies

        request_data = {'formTurma': 'formTurma',
                        'formTurma:inputNivel': level,
                        'formTurma:inputDepto': unity,
                        'formTurma:inputAno': year,
                        'formTurma:inputPeriodo': period,
                        'formTurma:j_id_jsp_1370969402_11': 'Buscar',
                        'javax.faces.ViewState': 'j_id1'}

        response = requests.post(cls._url, data=request_data,
                                 cookies=cls._cookies)

        return response.text

    @classmethod
    def __list_disciplines_by_soup(cls,
                                   soup: BeautifulSoup) -> list[Discipline]:
        disciplines: list[Discipline] = []

        for table_row in soup.find_all('tr', {'class': ['agrupador',
                                                        'linhaImpar',
                                                        'linhaPar']}):
            # Discipline data
            if table_row['class'] == ['agrupador']:
                code, name = table_row.find('span').text.split('-', maxsplit=1)
                disciplines.append(Discipline(id_=string_cleanup(code),
                                              name=string_cleanup(name)))

            # Offer data
            else:
                table_datas = table_row.findChildren('td', recursive=False)
                code = table_datas[0].text
                teacher = table_datas[2].text
                schedule = table_datas[3].text
                vacancies_offered = table_datas[5].text
                vacancies_occupied = table_datas[6].text
                place = table_datas[7].text

                disciplines[-1].add_offer(
                    Offer(code=string_cleanup(code),
                          teacher=string_cleanup(teacher),
                          schedule=cls.__parse_schedule(
                              string_cleanup(schedule)),
                          vacancy_filled=int(
                              string_cleanup(vacancies_occupied)),
                          vacancy_offered=int(
                              string_cleanup(vacancies_offered)),
                          place=string_cleanup(place))
                )

        return disciplines

    @classmethod
    def list_unities(cls) -> list[int]:
        if POSSIBLE_UNITIES:
            return POSSIBLE_UNITIES

        response = requests.get(cls._url)
        if not cls._cookies:
            cls._cookies = response.cookies

        soup = BeautifulSoup(response.content, 'html.parser')
        return cls.__list_unities_by_soup(soup)

    @classmethod
    def __list_unities_by_soup(cls, soup: BeautifulSoup) -> list[int]:
        select = soup.find('select', {'id': 'formTurma:inputDepto'})
        return [int(option['value'])
                # Skipping the first one, because it's just a placeholder
                for option in select.find_all('option')[1:]]  # type: ignore

    @staticmethod
    def __parse_schedule(schedule: str) -> Schedule:
        all_days = ['domingo', 'segunda', 'terça',
                    'quarta', 'quinta', 'sexta', 'sábado']

        parsed_schedule = re.sub(
            r'\s\d\d:\d\d às \d\d:\d\d(?=.*\d\d:\d\d às \d\d:\d\d)', ',',
            re.sub(r'(\d+\w\d+ )+((\(.+\)) )?', '', schedule))

        days, times = parsed_schedule.split(maxsplit=1)
        arrival_time, departure_time = times.split(' às ')
        return Schedule(
            days=[all_days.index(day.lower().replace('-feira', '')) for day in
                  days.split(',')],
            arrival=Time.from_string(arrival_time),
            departure=Time.from_string(departure_time))


def string_cleanup(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def get_html_filename(**kwargs) -> str:
    os.makedirs(HTML_PATH, exist_ok=True)
    return os.path.join(HTML_PATH, '{level}-{unity}-{year}-{period}.html'.format(**kwargs))

