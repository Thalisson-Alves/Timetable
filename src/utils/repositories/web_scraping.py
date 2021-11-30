import re

from bs4 import BeautifulSoup
from requests import Session

from utils.entities.discipline import Discipline
from utils.entities.offer import Offer
from utils.entities.schedule import Schedule, Time


def get_soup() -> BeautifulSoup:
    # Getting only offers from FGA for now
    disciplines_url = 'https://sig.unb.br/sigaa/public/turmas/listar.jsf'

    with Session() as session:
        response1 = session.get(disciplines_url)
        response2 = session.post(disciplines_url, headers={'User-Agent': 'insomnia/2021.6.0'},
                                 data={'formTurma': 'formTurma',
                                       'formTurma:inputNivel': 'G',
                                       'formTurma:inputDepto': '673',
                                       'formTurma:inputAno': '2021',
                                       'formTurma:inputPeriodo': '2',
                                       'formTurma:j_id_jsp_1370969402_11': 'Buscar',
                                       'javax.faces.ViewState': 'j_id1'},
                                 cookies=response1.cookies)

    return BeautifulSoup(response2.content, 'html.parser')


def load_disciplines() -> list[Discipline]:
    soup = get_soup()
    disciplines: list[Discipline] = []

    for table_row in soup.find_all('tr', {'class': ['agrupador', 'linhaImpar', 'linhaPar']}):
        # Discipline data
        if table_row['class'] == ['agrupador']:
            code, name = table_row.find('span').text.split(' - ')
            disciplines.append(Discipline(id_=string_cleanup(code),
                                          name=string_cleanup(name)))

        # Offer data
        else:
            table_datas = table_row.findChildren('td', recursive=False)
            code = table_datas[0].text
            teacher = table_datas[2].text
            schedule = table_datas[3].text
            vacancies_offered = table_datas[5].text
            vacancies_occuped = table_datas[6].text
            place = table_datas[7].text

            disciplines[-1].offers.append(
                Offer(code=string_cleanup(code),
                      teacher=string_cleanup(teacher),
                      schedule=parse_schedule(string_cleanup(schedule)),
                      vacancies_occuped=int(string_cleanup(vacancies_occuped)),
                      vacancies_offered=int(string_cleanup(vacancies_offered)),
                      place=string_cleanup(place))
            )

    return disciplines


def string_cleanup(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def parse_schedule(schedule: str) -> Schedule:
    all_days = ['domingo', 'segunda', 'terça',
                'quarta', 'quinta', 'sexta', 'sábado']

    parsed_schedule = re.sub(r'\s\d\d:\d\d às \d\d:\d\d(?=.*\d\d:\d\d às \d\d:\d\d)', ',',
                             re.sub(r'(\d+\w\d+ )+((\(.+\)) )?', '', schedule))

    days, times = parsed_schedule.split(maxsplit=1)
    arrival_time, departure_time = times.split(' às ')
    return Schedule(days=[all_days.index(day.lower().replace('-feira', '')) for day in days.split(',')],
                    arrival=Time.from_string(arrival_time),
                    departure=Time.from_string(departure_time))
