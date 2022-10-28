import streamlit as st
import pandas as pd

from client import new_client, DateRange

crime_api_client = new_client()

st.title("Crimes in Chicago")

date_range = crime_api_client.date_range()
print(date_range)
start_date = st.sidebar.date_input(
    "Start of date range:",
    date_range.end_date.replace(day=1),
    min_value=date_range.start_date,
    max_value=date_range.end_date,
)
end_date = st.sidebar.date_input(
    "End of date range:",
    date_range.end_date,
    min_value=start_date,
    max_value=date_range.end_date,
)

crime_types = st.sidebar.multiselect(
    "Crime types (all crime types shown if nothing chose):",
    crime_api_client.crime_types(),
)

with st.spinner("Fetching crimes data"):
    locations = crime_api_client.crime_locations(
        DateRange(start_date, end_date), crime_types or crime_api_client.crime_types()
    )
    if len(locations):
        st.success(f"Found {len(locations)} crime locations")
    else:
        st.success(f"No crime locations found")

    st.map(pd.DataFrame(locations))
