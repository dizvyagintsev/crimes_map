import datetime
from dataclasses import dataclass

from google.cloud import bigquery
from more_itertools import one


@dataclass
class DateRange:
    start_date: datetime.date
    end_date: datetime.date


@dataclass
class Location:
    latitude: float
    longitude: float


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

    def crime_locations(self, date_range: DateRange, crime_types: list[str]) -> list[Location]:
        """
        Returns a list of crime locations
        >>> range = DateRange(datetime.date(2022, 10, 1), datetime.date(2022, 10, 18))
        >>> ChicagoCrimesDAL(bigquery.Client()).crime_locations(range, )

        :param date_range: range of dates to query by
        :param crime_types: list of crime types to query by
        :return: list of locations
        """

        query = '''        
            SELECT latitude,
                longitude
            FROM `bigquery-public-data.chicago_crime.crime`
            WHERE x_coordinate IS NOT NULL
              AND y_coordinate IS NOT NULL
              AND DATE(date) BETWEEN @start_date AND @end_date
              AND primary_type in UNNEST(@crime_types);
        '''
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('start_date', 'DATE', date_range.start_date),
                bigquery.ScalarQueryParameter('end_date', 'DATE', date_range.end_date),
                bigquery.ArrayQueryParameter('crime_types', 'STRING', crime_types),
            ]
        )

        cursor = self.__session.query(query, job_config=job_config)

        return [Location(*row) for row in cursor]
