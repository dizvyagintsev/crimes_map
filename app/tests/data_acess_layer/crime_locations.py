from datetime import date
from unittest.mock import MagicMock

from google.cloud import bigquery
from google.cloud.bigquery import Row

from app.data_access_layer.crime_locations import ChicagoCrimesDAL


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
