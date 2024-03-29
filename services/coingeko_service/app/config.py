from pydantic_settings import BaseSettings
from pydantic import Field, Extra, AmqpDsn


class Config(BaseSettings):
    RABBITMQ_DSN: AmqpDsn = Field(
        default='amqp://guest:guest@localhost//',
        env='RABBITMQ_DSN',
        alias='RABBITMQ_DSN'
    )

    QUEUE_COINGEKO_NAME: str = Field(
        default='notification coingeko',
        env='QUEUE_COINGEKO_NAME',
        alias='QUEUE_COINGEKO_NAME'
    )

    COURSES_UPDATE_DELAY: int = Field(
        default=10,
        env='COURSES_UPDATE_DELAY',
        alias='COURSES_UPDATE_DELAY'
    )


    class Config:
        env_file = ".env"  # Указываем имя файла .env
        extra = Extra.allow  # Разрешаем дополнительные входные данные

# Создаем экземпляр конфигурации
def load_config() -> Config:
    return Config()