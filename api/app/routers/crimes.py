from fastapi import APIRouter, Depends

from api.app.data_access_layer.crime_locations import ChicagoCrimesDAL, DateRange, Location
from api.app.dependencies import get_chicago_crimes_dal

router = APIRouter(prefix='/api/crimes/chicago')


@router.get('/crime_types', response_model=list[str])
def get_crime_types(crimes_dal: ChicagoCrimesDAL = Depends(get_chicago_crimes_dal)):
    """
    List of possible crime types
    """
    return crimes_dal.crime_types()


@router.get('/date_range', response_model=DateRange)
def get_date_range(crimes_dal: ChicagoCrimesDAL = Depends(get_chicago_crimes_dal)):
    """
    First and last date from storage
    """
    return crimes_dal.date_range()


@router.get('/locations', response_model=list[Location])
def get_date_range(
        crime_types: list[str],
        date_range: DateRange,
        crimes_dal: ChicagoCrimesDAL = Depends(get_chicago_crimes_dal),
):
    """
    List of crime locations
    """
    return crimes_dal.crime_locations(date_range, crime_types)
