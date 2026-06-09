# My First Kafka Project: 🌤️ Weather Pipeline
This project is a self led pilot project which aims to help teach me kafka basics including docker and other technologies, having already built a foundation through university modules.

A real-time data pipeline built with Apache Kafka, Python, dbt, Snowflake and Streamlit.

The pipeline runs entirely with a single `docker-compose up` command.

## What it does

Fetches live weather data for Shoreham-by-Sea, UK from the **Open-Meteo API** every 60 seconds, streams it through Kafka, loads it into Snowflake, transforms it with dbt, and visualises it on a live Streamlit dashboard.

## Architecture

Open-Meteo API → Kafka Producer → Kafka Topic (weather) → Kafka Consumer → Snowflake → dbt → Streamlit Dashboard

## Tech Stack

| Technology | Description |
|------------|-------------|
| Apache Kafka (KRaft mode) | Message broker |
| Python | Producer and consumer scripts |
| Docker & Docker Compose | Containerisation and orchestration |
| Snowflake Init | Runs once on startup - creates all Snowflake objects if they don't exist |
| dbt | Runs dbt seed and dbt run to load reference data and build models |
| Streamlit | Live dashboard querying dbt models from Snowflake |

## How to run it

**Prerequisites:**
- Docker Desktop installed and running
- A Snowflake account (free 30 day trial at snowflake.com, no credit card required)

### Steps

**1. Clone the repo**
```bash
git clone https://github.com/oliverangel45/first-kafka-project.git
cd first-kafka-project
```

**2. Create your `.env` file**

Copy `.env.example` to `.env` and fill in your Snowflake credentials:
```bash
cp .env.example .env
```
```KAFKA_BROKER=broker:29092
SNOWFLAKE_ACCOUNT=your_account_identifier
SNOWFLAKE_USER=kafka_consumer
SNOWFLAKE_PASSWORD=your_kafka_consumer_password
SNOWFLAKE_ADMIN_USER=your_admin_username
SNOWFLAKE_ADMIN_PASSWORD=your_admin_password
SNOWFLAKE_DATABASE=weather_pipeline
SNOWFLAKE_SCHEMA=weather_data
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
```

**3. Start the pipeline**
```bash
docker-compose up --build
```

This will automatically:
- Start the Kafka broker
- Create all Snowflake objects (database, schema, table, roles, user)
- Start the producer fetching live weather data
- Start the consumer writing data to Snowflake
- Run dbt to load reference data and build transformed models
- Launch the Streamlit dashboard

**4. Open the dashboard**

Navigate to `http://localhost:8501` in your browser.

**5. Monitor the pipeline**
```bash
# Check producer is sending data
docker logs -f producer

# Check consumer is writing to Snowflake
docker logs -f consumer

# Check dbt models ran successfully
docker logs dbt

# Check Snowflake init completed
docker logs snowflake-init
```

**6. Stop the pipeline**
```bash
docker-compose down
```

## dbt Models

| Model | Type | Description |
|-------|------|-------------|
| stg_weather | View | Cleans raw data, renames columns, joins weathercode to human readable description |
| daily_averages | View | Average, max and min temperature and windspeed aggregated by day |
| latest_reading | View | Single most recent weather reading |

## What I learned

- How to build an end to end real time data pipeline from scratch
- Apache Kafka core concepts — brokers, topics, partitions, producers, consumers, offsets, KRaft mode
- I used this as a pilot project therefore I chose to create 1 broker with 1 Kafka topic - keeping things simple (for now)
- Writing Python Kafka producers and consumers using kafka-python
- Containerising Python applications with Docker and orchestrating multiple services with Docker Compose
- Docker concepts — images, containers, volumes, networking, layer caching, environment variables (Important and valuable new skills I have learned)
- Snowflake cloud data warehouse — databases, schemas, warehouses, roles, permissions, SQL
- dbt fundamentals — models, seeds, sources, Jinja templating, materialisation
- Streamlit for building live data dashboards in Python
- Managing sensitive credentials securely with .env files and .gitignore
- Debugging distributed systems across multiple containers
