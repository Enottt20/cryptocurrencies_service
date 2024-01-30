import asyncio
import httpx


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
        print("Received data:")
        for crypto, currencies in data.items():
            for currency, value in currencies.items():
                print(f'{crypto.upper()}-to-{currency.upper()}: {value}')
        print()

        if callback is not None:
            callback(data)


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


def callback_function(data):
    # Your logic to handle incoming data
    if data is not None:
        print("Callback function received data:", data)


def start_coingeko_service(callback):
    asyncio.run(fetch_and_send(callback=callback))

