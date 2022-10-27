from unittest.mock import MagicMock

from google.cloud import bigquery

from app.data_access_layer.crimes_locations import CrimeLocationsDAL


class TestCrimesLocationsDAL:
    def test_crime_types(self, mocked_session: bigquery.Client):
        mocked_session.query = MagicMock(
            return_value=[{'primary_type': 'DID NOT WRITE TESTS'}, {'primary_type': 'DID NOT USE TYPING'}]
        )

        assert CrimeLocationsDAL(mocked_session).crime_types() == ['DID NOT WRITE TESTS', 'DID NOT USE TYPING']
        mocked_session.query.assert_called_once_with(
            'SELECT DISTINCT(primary_type) FROM `bigquery-public-data.chicago_crime.crime`;'
        )
