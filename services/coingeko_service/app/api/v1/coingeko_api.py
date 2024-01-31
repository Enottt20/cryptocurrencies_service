import asyncio
import json

import httpx
from app.schemas import Course, ExchangeData


async def get_price(crypto, currency):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={currency}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

        if crypto in data and currency in data[crypto]:
            return data[crypto][currency]
        else:
            print(f"Error: Invalid response for {crypto}-to-{currency}")
            return None


async def send_data(data, callback=None):
    if data is not None:
        print("Получены данные:")
        exchange_data = []

        for crypto, currencies in data.items():
            for currency, value in currencies.items():
                # Проверяем, что значение является числом
                if isinstance(value, (int, float)):
                    # Преобразуем направления валютных пар
                    if crypto.lower() == 'tether':
                        crypto_abbr = 'USDT'
                    elif crypto.lower() == 'ethereum':
                        crypto_abbr = 'ETH'
                    elif crypto.lower() == 'bitcoin':
                        crypto_abbr = 'BTC'
                    else:
                        crypto_abbr = crypto.upper()

                    if currency.lower() == 'rub':
                        currency_abbr = 'RUB'
                    elif currency.lower() == 'usd':
                        currency_abbr = 'USD'
                    else:
                        currency_abbr = currency.upper()

                    direction = f"{crypto_abbr}-{currency_abbr}"
                    course = Course(direction=direction, value=value)
                    exchange_data.append(course)

                    print(f'{direction}: {value}')
                else:
                    print(f"Ошибка: Неверное значение для {crypto}-{currency}")

        print()

        # Создаем объект ExchangeData, содержащий информацию об обмене
        exchange_data_object = ExchangeData(exchanger="Coingeko", courses=exchange_data)

        if callback is not None:
            # Вызываем функцию обратного вызова с данными в формате ExchangeData
            await callback(json.dumps(exchange_data_object.dict(), indent=2))



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
        await asyncio.sleep(5)



def start_coingeko_service(callback):
    asyncio.run(fetch_and_send(callback=callback))

