from kombu import Connection, Exchange, Queue
import logging

logger = logging.getLogger(__name__)


class MessageProducer():
    def __init__(self, dsn, queue_name="notification", exchange_name="notification"):
        self.dsn = dsn
        self.queue_name = queue_name
        self.exchange = Exchange(exchange_name)
        self.queue = Queue(queue_name, exchange=self.exchange, routing_key=queue_name)

    def send_message(self, message):
        with Connection(self.dsn) as connection:
            producer = connection.Producer()
            producer.publish(message, exchange=self.exchange, routing_key=self.queue_name)
            logger.info(f'send message {message}')
