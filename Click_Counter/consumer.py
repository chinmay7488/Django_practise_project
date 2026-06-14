import json
import asyncio
import random
from channels.generic.websocket import AsyncWebsocketConsumer


class ClickerConsumer(AsyncWebsocketConsumer):
    global_count = 0
    active_connections = 0

    async def connect(self):
        self.room_group_name = 'counter_group'

        # Join the global broadcasting group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        ClickerConsumer.active_connections += 1
        self.broadcast_room_state()

    async def receive(self, text_data):
        
        # 1. Decode the raw JSON string from JavaScript into a Python dictionary
        data_json = json.loads(text_data)
        # 2. Extract the variables sent by the frontend
        action = data_json.get('action')

        if action == 'click_registered':
            ClickerConsumer.global_count += 1
        await self.broadcast_room_state()

    async def disconnect(self, text_data):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        ClickerConsumer.active_connections -= 1
        
        # 2. Immediately alert the remaining users so their screens update
        await self.broadcast_room_state()

    async def broadcast_room_state(self):
        """ Helper utility that packages the application state and shoots it to the group """
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_state_to_client',
                'count': ClickerConsumer.global_count,
                'users_online': ClickerConsumer.active_connections
            }
        )
    
    async def send_state_to_client(self, event):
        """ Receives the group broadcast data and pushes it over the live WebSocket tunnel to the browser """
        payload = {
            "current_count": event['count'],
            "users_online": event['users_online']
        }
        await self.send(text_data=json.dumps(payload))