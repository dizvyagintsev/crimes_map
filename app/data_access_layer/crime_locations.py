import datetime

from google.cloud import bigquery
from more_itertools import one


class ChicagoCrimesDAL:
    def __init__(self, session: bigquery.Client):
        self.__session = session

    def crime_types(self) -> list[str]:
        """
        Returns all crime types that exist in storage

        >>> ChicagoCrimesDAL(bigquery.Client()).crime_types()[:3]
        ['HOMICIDE', 'CRIM SEXUAL ASSAULT', 'CRIMINAL SEXUAL ASSAULT']

        :return: list of crime types as strings
        """
        query = 'SELECT DISTINCT(primary_type) FROM `bigquery-public-data.chicago_crime.crime`;'
        cursor = self.__session.query(query)

        return [row['primary_type'] for row in cursor]

    def date_range(self) -> tuple[datetime.date, datetime.date]:
        """
        Returns first and last crime date from storage

        >>> ChicagoCrimesDAL(bigquery.Client()).date_range()
        (datetime.date(2001, 1, 1), datetime.date(2022, 10, 18))

        :return: Two dates, min and max accordingly
        """
        query = 'SELECT MIN(DATE(date)), MAX(DATE(date)) FROM `bigquery-public-data.chicago_crime.crime`;'
        cursor = self.__session.query(query)

        return tuple(one(cursor))
