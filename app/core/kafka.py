import json
from typing import Optional
from aiokafka import AIOKafkaProducer  
import os
import asyncio

class KafkaProducer:
    _producer: Optional[AIOKafkaProducer] = None

    @classmethod
    async def start(cls, retries: int = 10, delay: int = 3):
        for attempt in range(retries):
            try:
                producer = AIOKafkaProducer(
                    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
                    value_serializer = lambda v: json.dumps(v).encode("utf-8")
                )
                await producer.start()
                cls._producer = producer  # ✅ só seta depois de conectar
                return
        
            except Exception as e:
                if attempt == retries - 1:
                    raise 
                await asyncio.sleep(delay)


    @classmethod
    async def stop(cls):
        if cls._producer:
            await cls._producer.stop()
            cls._producer = None
    
    @classmethod
    async def send(cls, topic: str, message: dict):
        if not cls._producer:
            await cls.start() 
    
        await cls._producer.send_and_wait(topic, message)
