from pydantic_settings import BaseSettings
from pydantic import Field, Extra, AmqpDsn


class Config(BaseSettings):

    RABBITMQ_DSN: AmqpDsn = Field(
        default='amqp://guest:guest@localhost//',
        env='RABBITMQ_DSN',
        alias='RABBITMQ_DSN'
    )

    QUEUE_RESERVATION_NAME: str = Field(
        default='notification apartment rental',
        env='QUEUE_RESERVATION_NAME',
        alias='QUEUE_RESERVATION_NAME'
    )

    QUEUE_REVIEW_NAME: str = Field(
        default='notification publish review',
        env='QUEUE_REVIEW_NAME',
        alias='QUEUE_REVIEW_NAME'
    )


    class Config:
        env_file = ".env"  # Указываем имя файла .env
        extra = Extra.allow  # Разрешаем дополнительные входные данные

# Создаем экземпляр конфигурации
def load_config() -> Config:
    return Config()

