import json
import asyncio
import random
from channels.generic.websocket import AsyncWebsocketConsumer

class TickerConsumer(AsyncWebsocketConsumer):
    # Keep track of running background loops globally so we don't start duplicate loops
    active_loops = {}

    async def connect(self):
        self.room_group_name = 'ticker_group'

        # Join the global broadcasting group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # If this is the very first user connecting, kick off the background price generator loop
        if self.room_group_name not in TickerConsumer.active_loops:
            TickerConsumer.active_loops[self.room_group_name] = asyncio.create_task(
                self.generate_live_prices()
            )

    async def disconnect(self, close_code):
        # Leave the broadcast group smoothly when a user closes their browser tab
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # --- THE SERVER-SIDE AUTOMATION PULSE ---
    async def generate_live_prices(self):
        """ This function runs in the background generating price fluctuations """
        prices = {
            "BTC": 65000.00,
            "ETH": 3500.00,
            "AAPL": 180.00,
            "TSLA": 250.00
        }
        
        try:
            while True:
                # 1. Simulate mock stock/crypto fluctuations
                for asset in prices:
                    change_percent = random.uniform(-0.02, 0.02) # -2% to +2%
                    prices[asset] = round(prices[asset] * (1 + change_percent), 2)

                # 2. Broadcast the fresh prices payload downward to the group layer
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'broadcast_ticker_data',
                        'data': prices
                    }
                )
                # 3. Pause for 1.5 seconds before repeating the infinite loop
                await asyncio.sleep(1.5)
                
        except asyncio.CancelledError:
            pass

    # This method handles receiving data from the group broadcast and throwing it out to the browser
    async def broadcast_ticker_data(self, event):
        prices_payload = event['data']
        await self.send(text_data=json.dumps(prices_payload))