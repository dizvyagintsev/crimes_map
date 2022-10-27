from unittest.mock import MagicMock

import pytest
from google.cloud import bigquery

from app.data_access_layer.crime_locations import CrimeLocationsDAL


@pytest.fixture
def mocked_session() -> bigquery.Client:
    return MagicMock(bigquery.Client)
