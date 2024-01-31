import asyncio
import json
import logging
import httpx
from app.schemas import Course, ExchangeData
from app import config

cfg: config.Config = config.load_config()

logger = logging.getLogger(__name__)


async def get_price(crypto, currency):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={currency}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

        if crypto in data and currency in data[crypto]:
            return data[crypto][currency]
        else:
            logger.error(f"Error: Invalid response for {crypto}-to-{currency}")
            return None


async def send_data(data, callback=None):
    if data is not None:
        exchange_data = create_exchange_data(data)
        exchange_data_object = create_exchange_data_object(exchange_data)

        if callback is not None:
            await invoke_callback(callback, exchange_data_object)


def create_exchange_data(data):
    exchange_data = []
    for crypto, currencies in data.items():
        for currency, value in currencies.items():
            if isinstance(value, (int, float)):
                crypto_abbr = map_crypto_abbr(crypto)
                currency_abbr = map_currency_abbr(currency)
                direction = f"{crypto_abbr}-{currency_abbr}"
                course = Course(direction=direction, value=value)
                exchange_data.append(course)
                logger.info(f'{direction}: {value}')
            else:
                logger.error(f"Ошибка: Неверное значение для {crypto}-{currency}")
    return exchange_data


def create_exchange_data_object(exchange_data):
    return ExchangeData(exchanger="Coingeko", courses=exchange_data)


async def invoke_callback(callback, exchange_data_object):
    await callback(json.dumps(exchange_data_object.dict(), indent=2))


def map_crypto_abbr(crypto):
    crypto_lower = crypto.lower()
    match crypto_lower:
        case 'tether':
            return 'USDT'
        case 'ethereum':
            return 'ETH'
        case 'bitcoin':
            return 'BTC'
        case _:
            return crypto.upper()


def map_currency_abbr(currency):
    currency_lower = currency.lower()
    match currency_lower:
        case 'rub':
            return 'RUB'
        case 'usd':
            return 'USD'
        case _:
            return currency.upper()


async def fetch_and_send(callback=None):
    cryptos = ['bitcoin', 'ethereum', 'tether']
    currencies = ['rub', 'usd']

    while True:
        tasks = []

        for crypto in cryptos:
            for currency in currencies:
                task = get_price(crypto, currency)
                tasks.append(task)

        results = await asyncio.gather(*tasks)

        data = {}
        for i in range(len(cryptos)):
            crypto_data = {
                currencies[0]: results[i * len(currencies)],
                currencies[1]: results[i * len(currencies) + 1]
            }
            data[cryptos[i]] = crypto_data

        await send_data(data, callback)
        await asyncio.sleep(cfg.COURSES_UPDATE_DELAY)



def start_coingeko_service(callback):
    asyncio.run(fetch_and_send(callback=callback))

