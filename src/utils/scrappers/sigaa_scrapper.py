import os
import re

import requests
from bs4 import BeautifulSoup
from requests.cookies import RequestsCookieJar

from utils.entities.discipline import Discipline
from utils.entities.offer import Offer
from utils.entities.schedule import Schedule, Time

CURRENT_YEAR = os.getenv('CURRENT_YEAR', 2022)
CURRENT_PERIOD = os.getenv('CURRENT_PERIOD', 1)


class SIGAAScrapper:
    _url = 'https://sig.unb.br/sigaa/public/turmas/listar.jsf'
    _cookies: RequestsCookieJar = None

    @classmethod
    def list_all_disciplines(cls):
        return [discipline for unity in cls.list_unities() for discipline in
                cls.list_disciplines(unity)]

    @classmethod
    def list_disciplines(cls, unity: int):
        print(f'Getting disciplines from unity: {unity}')
        soup = cls.__create_soup_for(unity, CURRENT_YEAR, CURRENT_PERIOD)
        return cls.__list_disciplines_by_soup(soup)

    @classmethod
    def __create_soup_for(cls, unity: int, year: str,
                          period: str, level: str = 'G') -> BeautifulSoup:
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
        return BeautifulSoup(response.content, 'html.parser')

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

                disciplines[-1].offers.append(
                    Offer(code=string_cleanup(code),
                          teacher=string_cleanup(teacher),
                          schedule=cls.__parse_schedule(
                              string_cleanup(schedule)),
                          vacancies_occupied=int(
                              string_cleanup(vacancies_occupied)),
                          vacancies_offered=int(
                              string_cleanup(vacancies_offered)),
                          place=string_cleanup(place))
                )

        return disciplines

    @classmethod
    def list_unities(cls) -> list[int]:
        response = requests.get(cls._url)
        if not cls._cookies:
            cls._cookies = response.cookies

        soup = BeautifulSoup(response.content, 'html.parser')
        return cls.__list_unities_by_soup(soup)

    @classmethod
    def __list_unities_by_soup(cls, soup: BeautifulSoup) -> list[int]:
        unities: list[int] = []
        select = soup.find('select', {'id': 'formTurma:inputDepto'})
        # Skipping the first one, because it's just a placeholder
        for option in select.find_all('option')[1:]:
            unities.append(int(option['value']))
        return unities

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
