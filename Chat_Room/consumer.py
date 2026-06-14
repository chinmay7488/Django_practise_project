import json
import asyncio
import random
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    active_user = 0
    Users =[]
    chat=[]

    async def connect(self):
        self.room_group_name='Chat_Room'
        # Join the global broadcasting group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        ChatConsumer.active_user += 1

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        # 2. Extract the variables sent by the frontend

        action = data_json.get('event')
        username = data_json.get('username')
        message = data_json.get('message')
        if action == 'message':
            if  username not in ChatConsumer.Users: 
                ChatConsumer.Users.append(username)
                await self.UserListUpdates()
            await self.MessageListUpdates(username, message, str(datetime.now()))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        ChatConsumer.active_user -= 1

    async def MessageListUpdates(self, username, message, time):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message_to_client',
                'username': username,
                'message': message,
                'timestamp' : time
            }
        )

    async def UserListUpdates(self):   
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_user_list_to_client',
                'users' : ChatConsumer.Users
            }
        )
    
    async def send_message_to_client(self, event):
        payload = {
                'type' : 'chat_message',
                'username': event['username'],
                'message': event['message'],
                'timestamp' : event['timestamp']
        }
        await self.send(text_data=json.dumps(payload))

    async def send_user_list_to_client(self, event):
        payload = {
                'type' : 'user_list',
                'users': event['users']
        }
        await self.send(text_data=json.dumps(payload))


