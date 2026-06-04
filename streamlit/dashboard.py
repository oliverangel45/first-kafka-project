import streamlit as st
import snowflake.connector
import pandas as pd
import os
import time

# Snowflake Creds
SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_USER = os.environ.get('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.environ.get('SNOWFLAKE_PASSWORD')
SNOWFLAKE_DATABASE = os.environ.get('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.environ.get('SNOWFLAKE_SCHEMA')
SNOWFLAKE_WAREHOUSE = os.environ.get('SNOWFLAKE_WAREHOUSE')

def get_snowflake_connection():
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        warehouse=SNOWFLAKE_WAREHOUSE
    )
    conn.cursor().execute("USE WAREHOUSE COMPUTE_WH")
    return conn

# Runs any query against Snowflake and returns results as DataFrame
def run_query(query):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(data, columns=columns)


# Page Config
st.set_page_config(
    page_title="Shoreham-by-Sea Weather Dashbaord",
    page_icon="🌤️",
    layout="wide"
)
st.title("🌤️ Shoreham-by-Sea Weather Dashboard")
st.caption("Live weather data powered by Open-Meteo API via Kafka and Snowflake")
st.subheader("Current Conditions")

latest = run_query("SELECT * FROM weather_pipeline.weather_data.latest_reading") # DataFrame with 1 row


# Metric Cards
if not latest.empty:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Temperature", f"{latest['TEMPERATURE_CELSIUS'].values[0]}°C") 
    with col2:
        st.metric("Wind Speed", f"{latest['WINDSPEED_KMH'].values[0]} km/h")      
    with col3:
        st.metric("Wind Direction", f"{latest['WIND_DIRECTION_DEGREES'].values[0]}°")   
    with col4:
        st.metric("Conditions", latest['WEATHER_DESCRIPTION'].values[0])
        
else:
    st.warning("No current weather data available")

   
# Temp Chart
st.subheader("Temperature Over Time")

temp_data = run_query("""
    SELECT observation_time, temperature_celsius
    FROM weather_pipeline.weather_data.stg_weather
    ORDER BY observation_time ASC
""")

if not temp_data.empty:
    st.line_chart(temp_data.set_index('OBSERVATION_TIME')['TEMPERATURE_CELSIUS'])
else:
    st.warning("No temperature history available")


# Daily Average Table
st.subheader("Daily Averages")

daily = run_query("""
    SELECT 
        observation_date,
        avg_temperature_celsius,
        max_temperature_celsius,
        min_temperature_celsius,
        avg_windspeed_kmh,
        reading_count
    FROM weather_pipeline.weather_data.daily_averages
    ORDER BY observation_date DESC
""")

if not daily.empty:
    st.dataframe(daily, use_container_width=True)
else:
    st.warning("No daily averages available")


# Auto Refresh
st.caption(f"Dashboard auto-refreshes every 60 seconds")
time.sleep(60)
st.rerun()