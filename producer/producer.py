import json
import time
import requests
from kafka import KafkaProducer

KAFKA_TOPIC = 'weather'
KAFKA_BROKER = 'broker:29092'
# Shoreham By-Sea Coordinates
LATITUDE = 50.8279
LONGITUDE = -0.2752

def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"
    response = requests.get(url)
    return response.json()

def main():
    # Allow Kafka to start
    print ("Waiting for Kafka to start up")
    time.sleep(15)
    
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    while True:
        weather = get_weather()
        print(f"Sending: {weather}")
        producer.send(KAFKA_TOPIC, value=weather)
        time.sleep(60) #Fetches and sends weather data to topic once per minute
    
if __name__ == '__main__':
    main()