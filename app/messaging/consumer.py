import json 
import threading
from confluent_kafka import Consumer
from app.core.config import settings
from app.messaging.handlers import handle_motorcycle_created

def _consumer_loop():
    consumer = Consumer(
        {
            "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
            "group.id": settings.KAFKA_CONSUMER_GROUP,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True
        }
    )

    consumer.subscribe([settings.KAFKA_MOTORCYCLE_TOPIC])

    try: 
        while True:

            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(f"[KAFKA ERROR] {msg.error()}")
                continue

            event = json.loads(msg.value().decode("utf-8"))
            handle_motorcycle_created(event)

    except Exception as e:
        print(f"[CONSUMER ERROR] {e}")
    
    finally:
        consumer.close()


def start_motorcycle_consumer() -> None:
    thread = threading.Thread(target = _consumer_loop, daemon = True)
    thread.start()