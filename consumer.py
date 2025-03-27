from kafka import KafkaConsumer
from database import insert
import json
import time

def consume_from_kafka(topic, running):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='recipe-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("Consumer started. Waiting for messages...")

    while running[0]:
        try:
            messages = consumer.poll(timeout_ms=100)
            for tp, messages in messages.items():
                for message in messages:
                    process_recipe(message.value)
        except Exception as e:
            print(f"Error while consuming messages: {e}")
            time.sleep(1)

    consumer.close()
    print("Consumer has been closed.")

def process_recipe(recipe):
    insert([recipe])