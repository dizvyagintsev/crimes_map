from google.cloud import bigquery

from api.app.data_access_layer.crime_locations import ChicagoCrimesDAL


def get_chicago_crimes_dal():
    yield ChicagoCrimesDAL(bigquery.Client())
