## Запуск в docker compose
Для запуска нужно прописать данную комманду в директории Deploy предварительно запустив docker и создав файл конфигурации
```ini
docker compose up -d
```

```ini
RABBITMQ_USER=guest
RABBITMQ_PASS=guest
QUEUE_BINANCE_NAME=notification binance
QUEUE_COINGEKO_NAME=notification coingeko
RABBITMQ_DSN=amqp://guest:guest@rabbitmq//
REDIS_URL=redis://redis:6379
COURSES_UPDATE_DELAY=10
```

Работает только для Coingeko. Бинанс обновляется раз в секунду
```ini
COURSES_UPDATE_DELAY
```