from datetime import date
from unittest.mock import MagicMock

from google.cloud import bigquery
from google.cloud.bigquery import Row
from more_itertools import one

from app.data_access_layer.crime_locations import ChicagoCrimesDAL, DateRange, Location


class TestChicagoCrimesDAL:
    def test_crime_types(self, mocked_session: bigquery.Client):
        mocked_session.query = MagicMock(
            return_value=[
                Row(('DID NOT WRITE TESTS',), {'primary_type': 0}),
                Row(('DID NOT USE TYPING',), {'primary_type': 0})
            ],
        )

        assert ChicagoCrimesDAL(mocked_session).crime_types() == ['DID NOT WRITE TESTS', 'DID NOT USE TYPING']
        mocked_session.query.assert_called_once_with(
            'SELECT DISTINCT(primary_type) FROM `bigquery-public-data.chicago_crime.crime`;'
        )

    def test_date_ranges(self, mocked_session: bigquery.Client):
        mocked_session.query = MagicMock(
            return_value=[Row((date(2001, 1, 1), date(2022, 10, 18)), {'f0_': 0, 'f1_': 1})],
        )

        assert ChicagoCrimesDAL(mocked_session).date_range() == (date(2001, 1, 1), date(2022, 10, 18))
        mocked_session.query.assert_called_once_with(
            'SELECT MIN(DATE(date)), MAX(DATE(date)) FROM `bigquery-public-data.chicago_crime.crime`;'
        )

    def test_locations(self, mocked_session: bigquery.Client):
        mocked_session.query = MagicMock(
            return_value=[Row((41.694312336, -87.631090274), {'latitude': 0, 'longitude': 1})],
        )

        date_range = DateRange(date(2022, 10, 1), date(2022, 10, 18))
        assert ChicagoCrimesDAL(mocked_session).crime_locations(date_range, ['HOMICIDE']) == [
            Location(latitude=41.694312336, longitude=-87.631090274),
        ]

        query = '''        
            SELECT latitude,
                longitude
            FROM `bigquery-public-data.chicago_crime.crime`
            WHERE x_coordinate IS NOT NULL
              AND y_coordinate IS NOT NULL
              AND DATE(date) BETWEEN @start_date AND @end_date
              AND primary_type in UNNEST(@crime_types);
        '''
        call = one(mocked_session.query.mock_calls)
        assert one(call.args) == query
        assert call.kwargs['job_config'].query_parameters == [
            bigquery.ScalarQueryParameter('start_date', 'DATE', date(2022, 10, 1)),
            bigquery.ScalarQueryParameter('end_date', 'DATE', date(2022, 10, 18)),
            bigquery.ArrayQueryParameter('crime_types', 'STRING', ['HOMICIDE']),
        ]
        assert len(call.kwargs) == 1
