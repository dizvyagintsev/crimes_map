from unittest.mock import MagicMock

from google.cloud import bigquery
from google.cloud.bigquery import Row

from app.data_access_layer.crime_locations import CrimeLocationsDAL


class TestCrimeLocationsDAL:
    def test_crime_types(self, mocked_session: bigquery.Client):
        mocked_session.query = MagicMock(
            return_value=[
                Row(('DID NOT WRITE TESTS',), {'primary_type': 0}),
                Row(('DID NOT USE TYPING',), {'primary_type': 0})
            ],
        )

        assert CrimeLocationsDAL(mocked_session).crime_types() == ['DID NOT WRITE TESTS', 'DID NOT USE TYPING']
        mocked_session.query.assert_called_once_with(
            'SELECT DISTINCT(primary_type) FROM `bigquery-public-data.chicago_crime.crime`;'
        )