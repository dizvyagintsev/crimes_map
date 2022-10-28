# Chicago crimes map

Dashboard for visualization data from `bigquery-public-data.chicago_crime.crime`. Built with [Streamlit](https://github.com/streamlit/streamlit) and [FastAPI](https://github.com/tiangolo/fastapi).

![interface](screenshots/dashboard.png)

## How to run
1. Create a service user in the google cloud console
2. Generate JSON with credentials
3. Put your credentials to api/credentials/credentials.json
4. Run `docker-compose up --build` in the root of the repo

The dashboard will be available at http://0.0.0.0:8501 and API at http://0.0.0.0:8000. After deploying an API you can find 
docs at http://0.0.0.0:8000/docs#/

## How to make it better
Here is a list of things that could be improved in this dashboard:

- [ ] Better caching. Now I am using a simple st.cache that doesn't work if we change the dates interval a bit (for example 
by adding one extra day). We can use more complex caching on the API side, store locations grouped by date and type in Redis 
, and join data from cache with data from bigquery
- [ ] Better map. `streamlit.map` is too simple. So if in the future we would like to add different markers on the map, or
add pop-ups, or build a heatmap we should use another map.
- [ ] OAuth's authentication so every client will not use one credential stored on the server
