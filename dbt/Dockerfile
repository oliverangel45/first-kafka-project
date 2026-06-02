FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dbt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy dbt project
COPY weather_dbt/ ./weather_dbt/

# Copy profiles
COPY profiles.yml ./profiles.yml

ENV DBT_PROFILES_DIR=/app

CMD ["sh", "-c", "dbt seed --project-dir weather_dbt && dbt run --project-dir weather_dbt"]