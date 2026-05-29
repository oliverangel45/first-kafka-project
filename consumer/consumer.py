import json
import time
from kafka import KafkaConsumer
import snowflake.connector
import os

# Variables
KAFKA_TOPIC = 'weather'
KAFKA_BROKER = os.environ.get('KAFKA_BROKER')
GROUP_ID = 'weather-consumer-group'

# Snowflake Config (using .env file)
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
        schema= SNOWFLAKE_SCHEMA,
        warehouse=SNOWFLAKE_WAREHOUSE
    )
    conn.cursor().execute("USE WAREHOUSE COMPUTE_WH")
    return conn
    
def insert_weather(cursor, weather):
    current = weather.get('current_weather', {})
    cursor.execute("""
        INSERT INTO weather_readings (
            latitude,
            longitude,
            temperature,
            windspeed,
            winddirection,
            weathercode,
            is_day,
            observation_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        weather.get('latitude'),
        weather.get('longitude'),
        current.get('temperature'),
        current.get('windspeed'),
        current.get('winddirection'),
        current.get('weathercode'),
        current.get('is_day'),
        current.get('time')
    ))
    

def main():
    print("Waiting for Kafka to start up")
    time.sleep(15)
    
    print("Connecting to Snowflake...")
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    print("Connected to Snowflake successfully")
    
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id=GROUP_ID,
        auto_offset_reset='earliest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    
    for message in consumer:
        weather = message.value
        print(f"Received: {weather}")
        insert_weather(cursor, weather)
        conn.commit()
        print("Inserted into Snowflake sucessfully")
    
if __name__ == '__main__':
    main() 