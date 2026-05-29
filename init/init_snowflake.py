import snowflake.connector
import os
import time

# Snowflake constants
SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_ADMIN_USER = os.environ.get('SNOWFLAKE_ADMIN_USER')
SNOWFLAKE_ADMIN_PASSWORD = os.environ.get('SNOWFLAKE_ADMIN_PASSWORD')
SNOWFLAKE_DATABASE = os.environ.get('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.environ.get('SNOWFLAKE_SCHEMA')
SNOWFLAKE_WAREHOUSE = os.environ.get('SNOWFLAKE_WAREHOUSE')

def get_snowflake_connection():
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_ADMIN_USER,
        password=SNOWFLAKE_ADMIN_PASSWORD,
        warehouse='COMPUTE_WH'
    )
    conn.cursor().execute("USE WAREHOUSE COMPUTE_WH")
    return conn

def init_snowflake():
    # Connect to Snowflake as admin
    print("Connecting to Snowflake as admin...")
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    print("Connected successfully!")
    
    # Create the database and schema
    print("Creating database and schema if not exists...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {SNOWFLAKE_DATABASE}")
    cursor.execute(f"USE DATABASE {SNOWFLAKE_DATABASE}")
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {SNOWFLAKE_SCHEMA}")
    cursor.execute(f"USE SCHEMA {SNOWFLAKE_SCHEMA}")
    
    # Create weather_readings table
    print("Creating table if not exists...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_readings (
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            winddirection FLOAT,
            weathercode INT,
            is_day INT,
            observation_time TIMESTAMP
        )               
    """)
    
    # Create role, user and grant permissions
    print("Creating role and user if not exists...")
    
    cursor.execute("CREATE ROLE IF NOT EXISTS kafka_consumer_role")
    
    cursor.execute(f"GRANT USAGE ON DATABASE {SNOWFLAKE_DATABASE} TO ROLE kafka_consumer_role")
    cursor.execute(f"GRANT USAGE ON SCHEMA {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA} TO ROLE kafka_consumer_role")
    cursor.execute(f"GRANT INSERT ON TABLE {SNOWFLAKE_DATABASE}.{SNOWFLAKE_SCHEMA}.weather_readings TO ROLE kafka_consumer_role")
    cursor.execute("GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE kafka_consumer_role")
    
    snowflake_user = os.environ.get('SNOWFLAKE_USER')
    snowflake_password = os.environ.get('SNOWFLAKE_PASSWORD')
    
    cursor.execute(f"""
        CREATE USER IF NOT EXISTS {snowflake_user}
        PASSWORD = '{snowflake_password}'
        DEFAULT_ROLE = kafka_consumer_role
        DEFAULT_WAREHOUSE = COMPUTE_WH
    """)
    
    cursor.execute(f"GRANT ROLE kafka_consumer_role to USER {snowflake_user}")
    cursor.execute(f"ALTER USER {snowflake_user} SET TIMEZONE = 'UTC'")
    cursor.execute("ALTER WAREHOUSE COMPUTE_WH SET AUTO_SUSPEND = 120")
    cursor.execute("ALTER WAREHOUSE COMPUTE_WH SET AUTO_RESUME = TRUE")
    
    conn.commit()
    cursor.close()
    print("Snowflake initialisation complete")

if __name__ == '__main__':
    init_snowflake()