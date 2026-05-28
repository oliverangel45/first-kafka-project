FROM python:3.12-slim

# Set environment variable to prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY consumer.py .

CMD ["python", "consumer.py"]