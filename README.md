# My First Kafka Project: Weather Pipeline
This project is a self led pilot project which aims to help teach me kafka basics including docker and other technologies.

A real-time data pipeline built with Apache Kafka and Python, running entirely in Docker.

## What it does

Fetches live weather data for Shoreham-by-Sea, UK from the Open-Meteo API every 60 seconds, publishes it to a Kafka topic, and consumes it in real time.

## Architecture

Open-Meteo API → Producer → Kafka Topic (weather) → Consumer

## Tech Stack

- **Apache Kafka** (KRaft mode) — message broker
- **Python** — producer and consumer scripts
- **Docker & Docker Compose** — containerisation and orchestration
- **Open-Meteo API** — free real time weather data, no API key required

## Project Structure

first-kafka-project/
├── docker-compose.yml
├── producer/
│   ├── producer.py
│   ├── requirements.txt
│   └── Dockerfile
└── consumer/
├── consumer.py
├── requirements.txt
└── Dockerfile

## How to run it

**Prerequisites:**
- Docker Desktop installed and running

**Steps:**

1. Clone the repo
```bash
git clone https://github.com/oliverangel45/first-kafka-project.git
cd first-kafka-project
```

2. Start all services
```bash
docker-compose up --build
```

3. Check the producer is sending data
```bash
docker logs -f producer
```

4. Check the consumer is receiving data
```bash
docker logs -f consumer
```

5. To stop all services
```bash
docker-compose down
```

## What I learned

- How to run Apache Kafka locally using Docker Compose in KRaft mode (no Zookeeper)
- How to write a Python Kafka producer that fetches data from a REST API and publishes messages to a topic
- How to write a Python Kafka consumer that reads and deserializes messages from a topic
- How to containerise Python applications using Docker and wire them together with Docker Compose
- Docker concepts including images, containers, volumes, networking, and layer caching

## What's next

- Land the consumed data into a cloud data warehouse (Snowflake or BigQuery)
- Add data transformation before loading
- Add Airflow to orchestrate the pipeline