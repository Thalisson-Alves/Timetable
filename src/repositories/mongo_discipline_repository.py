from urllib.parse import quote_plus

from pymongo import MongoClient

from models import Discipline, Offer, Schedule, Time
from utils.settings import (MONGO_USER, MONGO_PASSWORD, MONGO_HOST,
                            CURRENT_YEAR, CURRENT_PERIOD)


class MongoDisciplineRepository:
    def __init__(self):
        uri = "mongodb://%s:%s@%s" % (
            quote_plus(MONGO_USER), quote_plus(MONGO_PASSWORD), MONGO_HOST)
        self.client = MongoClient(uri)
        self.db = self.client['timetable']
        self.collection = self.db['disciplines']

    def has_any_entry(self) -> bool:
        filters = {'year': CURRENT_YEAR, 'period': CURRENT_PERIOD}
        return self.collection.count_documents(filters) > 0

    def create(self, disciplines: list[Discipline]) -> None:
        # TODO: save the disciplines in different documents
        semester = [{'year': CURRENT_YEAR,
                     'period': CURRENT_PERIOD,
                     **self.__convert_discipline_to_db(discipline)}
                    for discipline in disciplines]

        self.collection.insert_many(semester)

    def get_all(self, filters: dict = None) -> list[Discipline]:
        if filters is None:
            filters = {}

        filters['year'] = CURRENT_YEAR
        filters['period'] = CURRENT_PERIOD

        results = self.collection.find(filters)
        return [*map(self.__convert_db_to_discipline, results)]

    @classmethod
    def __convert_discipline_to_db(cls, discipline: Discipline) -> dict:
        return {**discipline.__dict__,
                'offers': [*map(cls.__convert_offer_to_db,
                                discipline.offers)]}

    @classmethod
    def __convert_offer_to_db(cls, offer: Offer) -> dict:
        return {**offer.__dict__,
                'schedule': cls.__convert_schedule_to_db(offer.schedule)}

    @classmethod
    def __convert_schedule_to_db(cls, schedule: Schedule) -> dict:
        return {**schedule.__dict__,
                'arrival': {**schedule.arrival.__dict__},
                'departure': {**schedule.departure.__dict__}}

    @classmethod
    def __convert_db_to_discipline(cls, result: dict) -> Discipline | None:
        if not result:
            return None

        invalid_keys = [k for k in result if k not in
                        getattr(Discipline, '__dataclass_fields__')]
        for key in invalid_keys:
            result.pop(key, None)

        result['offers'] = [*map(cls.__convert_db_to_offer, result['offers'])]
        return Discipline(**result)

    @classmethod
    def __convert_db_to_offer(cls, result: dict) -> Offer | None:
        if not result:
            return None

        result['schedule'] = cls.__convert_db_to_schedule(result['schedule'])
        return Offer(**result)

    @classmethod
    def __convert_db_to_schedule(cls, result: dict) -> Schedule | None:
        if not result:
            return None

        result['arrival'] = Time(**result['arrival'])
        result['departure'] = Time(**result['departure'])
        return Schedule(**result)
