import aio_pika
import asyncio
from logging import getLogger

logger = getLogger("notification-service")

class Consumer:
    def __init__(self, dsn, queue_name="notification", exchange_name="notification"):
        self.dsn = dsn
        self.callbacks = []
        self.queue_name = queue_name

    def add_callback(self, callback):
        async def wrapped_callback(body):
            try:
                logger.info(f"Received data - {body}")
                await callback(body)
            except Exception as e:
                logger.error('Received data error!!!')

        self.callbacks.append(wrapped_callback)

    async def run(self):
        # Установка соединения с RabbitMQ
        connection = await aio_pika.connect_robust(self.dsn)

        # Создание канала
        async with connection:
            channel = await connection.channel()

            # Объявление очереди
            queue_name = self.queue_name

            queue_arguments = {
                "x-max-length": 1,
                "x-overflow": "drop-head"
            }

            queue = await channel.declare_queue(queue_name, durable=True, arguments=queue_arguments)

            async for message in queue:
                async with message.process():
                    task = message.body.decode()
                    for callback in self.callbacks:
                        await callback(task)

