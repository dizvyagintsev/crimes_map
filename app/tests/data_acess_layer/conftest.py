from unittest.mock import MagicMock

import pytest
from google.cloud import bigquery


@pytest.fixture
def mocked_session() -> bigquery.Client:
    return MagicMock(bigquery.Client)
