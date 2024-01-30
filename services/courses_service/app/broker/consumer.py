from kombu import Connection, Exchange, Queue, Consumer
from socket import timeout as timeout_err
from logging import getLogger

logger = getLogger("notification-service")


class Consumer():
    def __init__(self, dsn, queue_name="notification", exchange_name="notification"):
        self.dsn = dsn
        self.callbacks = []
        self.exchange = Exchange(exchange_name)
        self.queue = Queue(queue_name, exchange=self.exchange, routing_key=queue_name)
        self.queue_name = queue_name

    def process_message(self, body, message):
        try:
            logger.info(f"Received data - {body}")
        finally:
            message.ack()

    def add_callback(self, callback):
        def wrapped_callback(body):
            try:
                logger.info(f"Received data - {body}")
                callback(body)
            except:
                logger.error('Received data error!!!')

        self.callbacks.append(wrapped_callback)

    def run(self):
        if not self.callbacks:
            raise ValueError("No callbacks are registered. Add callbacks using add_callback method.")

        with Connection(self.dsn) as connection:
            with connection.Consumer(self.queue, callbacks=self.callbacks) as consumer:
                logger.info("Started pooling messages")
                while True:
                    try:
                        connection.drain_events(timeout=10)
                    except timeout_err:
                        connection.heartbeat_check()
