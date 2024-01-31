import asyncio
import logging
import websockets
import json
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
logger = logging.getLogger(__name__)


class BinanceWebSocketClient:
    def __init__(self, params):
        self.socket_url = "wss://stream.binance.com:9443/ws"
        self.params = params
        self.ws = None
        self.candle_datas = []

    async def on_message(self, message):
        data = json.loads(message)
        if 'k' in data:
            candle = data['k']
            close_price = candle['c']
            timestamp = candle['t']
            ticker = candle['s']

            time_str = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            candle_data = {
                'direction': ticker,
                #'time': time_str,
                'value': close_price
            }

            self.candle_datas.append(candle_data)

    async def on_open(self, ws):
        payload = {
            "method": "SUBSCRIBE",
            "params": self.params,
            "id": 1
        }
        await ws.send(json.dumps(payload))

    async def connect(self):
        try:
            async with websockets.connect(self.socket_url) as ws:
                await self.on_open(ws)

                async def receive_forever():
                    try:
                        while True:
                            message = await ws.recv()
                            await self.on_message(message)
                    except websockets.exceptions.ConnectionClosed as e:
                        logger.error(e)

                receive_task = asyncio.create_task(receive_forever())

                stop_event = asyncio.Event()
                while not stop_event.is_set():
                    self.candle_datas = []
                    await asyncio.sleep(1)

                receive_task.cancel()
                await asyncio.gather(receive_task, return_exceptions=True)
        except Exception as e:
            print(f"An error occurred during connection: {e}")

    def get_candles_data(self):
        return self.candle_datas


async def run_binance_websocket(client: BinanceWebSocketClient):
    await client.connect()


async def send_data(client: BinanceWebSocketClient, callback):
    while True:
        await callback(client.candle_datas)
        await asyncio.sleep(1)


def run_binance_subscription(subscription_params, callback):
    client = BinanceWebSocketClient(subscription_params)
    loop = asyncio.get_event_loop()

    tasks = [
        loop.create_task(run_binance_websocket(client)),
        loop.create_task(send_data(client, callback)),
    ]

    loop.run_until_complete(asyncio.gather(*tasks))
