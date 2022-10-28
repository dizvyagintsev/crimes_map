import datetime
import os
from dataclasses import dataclass
import streamlit as st

from yarl import URL
import requests


@dataclass
class DateRange:
    start_date: datetime.date
    end_date: datetime.date


class CrimesAPIClient:
    def __init__(self, host: URL):
        self.__root = host / "api" / "crimes" / "chicago"

    @st.cache
    def crime_types(self) -> list[str]:
        """
        Returns all crime types that exist in storage

        >>> CrimesAPIClient(URL('host')).crime_types()[:3]
        ['HOMICIDE', 'CRIM SEXUAL ASSAULT', 'CRIMINAL SEXUAL ASSAULT']

        :return: list of crime types as strings
        """
        return requests.get(str(self.__root / "crime_types")).json()

    @st.cache
    def date_range(self) -> DateRange:
        """
        Returns first and last crime date from storage

        >>> CrimesAPIClient(URL('host')).date_range()
        DateRange(datetime.date(2001, 1, 1), datetime.date(2022, 10, 18))

        :return: Struct with first and last date
        """
        json_ = requests.get(str(self.__root / "date_range")).json()
        return DateRange(
            start_date=datetime.datetime.fromisoformat(json_["start_date"]),
            end_date=datetime.datetime.fromisoformat(json_["end_date"]),
        )

    @st.cache
    def crime_locations(
        self, date_range: DateRange, crime_types: list[str]
    ) -> list[dict[str, float]]:
        """
        Returns a list of crime locations
        >>> dates = DateRange(datetime.date(2022, 10, 1), datetime.date(2022, 10, 18))
        >>> CrimesAPIClient(URL('host')).crime_locations(dates, ['HOMICIDE'])
        [{"latitude": 40.1, "longitude": -80.2}]

        :param date_range: range of dates to query by
        :param crime_types: list of crime types to query by
        :return: list of locations
        """
        url = (
            self.__root
            / "locations"
            % {
                "start_date": date_range.start_date.isoformat(),
                "end_date": date_range.end_date.isoformat(),
                "crime_types": crime_types,
            }
        )

        return requests.get(str(url)).json()


@st.cache
def new_client():
    return CrimesAPIClient(URL(os.environ["API_HOST"]))
