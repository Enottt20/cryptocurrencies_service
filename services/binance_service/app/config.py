from pydantic_settings import BaseSettings
from pydantic import Field, Extra, AmqpDsn


class Config(BaseSettings):

    SMTP_SERVER: str = Field(
        default='smtp.yandex.com',
        env='SMTP_SERVER',
        alias='SMTP_SERVER'
    )

    SMTP_PORT: int = Field(
        default='587',
        env='SMTP_PORT',
        alias='SMTP_PORT'
    )

    EMAIL_LOGIN: str = Field(
        default='yantestsss22@yandex.ru',
        env='EMAIL_LOGIN',
        alias='EMAIL_LOGIN'
    )

    EMAIL_PASSWORD: str = Field(
        default='pfxgsdpenvktcvtv',
        env='EMAIL_PASSWORD',
        alias='EMAIL_PASSWORD'
    )

    IS_SMPT_SSL: bool = Field(
        default=False,
        env='IS_SMPT_SSL',
        alias='IS_SMPT_SSL'
    )

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

