import asyncio
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
import os

KAFKA_TOPICS = [
    {
        "name": os.getenv("KAFKA_MOTORCYCLE_TOPIC"),
        "partitions": 1,
        "replication_factor": 1
    }
]

async def ensure_kafka_topics(retries: int = 10, delay: int = 3) -> None:
    admin = AIOKafkaAdminClient(
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    )

    for attempt in range(retries):
        try:
            await admin.start()

            existing_topics = await admin.list_topics()

            topics_to_create = [
                NewTopic(
                    name = t["name"],
                    num_partitions = t["partitions"],
                    replication_factor = t["replication_factor"]
                )
                for t in KAFKA_TOPICS
                if t["name"] not in existing_topics
            ]

            if topics_to_create: 
                await admin.create_topics(topics_to_create)

            return
        
        except Exception:
            if attempt == retries - 1:
                raise 

            await asyncio.sleep(delay)

        finally:
            await admin.close()
