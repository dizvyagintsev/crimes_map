from google.cloud import bigquery


class CrimeLocationsDAL:
    def __init__(self, session: bigquery.Client):
        self.__session = session
        # self.__session = session

    def crime_types(self) -> list[str]:
        """
        Returns all crime types that exist in storage

        >>> CrimeLocationsDAL(bigquery.Client()).crime_types()[:3]
        ['HOMICIDE', 'CRIM SEXUAL ASSAULT', 'CRIMINAL SEXUAL ASSAULT']

        :return: list of crime types as strings
        """
        query = 'SELECT DISTINCT(primary_type) FROM `bigquery-public-data.chicago_crime.crime`;'
        cursor = self.__session.query(query)

        return [row['primary_type'] for row in cursor]
