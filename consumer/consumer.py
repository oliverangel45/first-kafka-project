import json
import time
from kafka import KafkaConsumer

KAFKA_TOPIC = 'weather'
KAFKA_BROKER = 'broker:29092'
GROUP_ID = 'weather-consumer-group'

def main():
    print("Waiting for Kafka to start up")
    time.sleep(15)
    
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
    
if __name__ == '__main__':
    main() 