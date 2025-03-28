from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def send_to_kafka(topic, recipes):
    for recipe in recipes:
        producer.send(topic, value=recipe)
    producer.flush()