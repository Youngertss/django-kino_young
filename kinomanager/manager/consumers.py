import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.user_main_name = self.scope["user"]
        
        self.chat_id = await self.init_connect()
        
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        print("Disconnect")
    
    @database_sync_to_async
    def init_connect(self):
        self.user_main = KinoUsers.objects.get(username=self.scope["user"])
        self.user__username = self.user_main.username
        
        if not self.user_main.is_support:
            self.user = self.user_main
            users_supports = KinoUsers.objects.filter(is_support=True)
            self.user_support = users_supports.order_by('?').first()
        else:
            self.user_support =  self.user_main
            self.user = self.user_support
            print(self.scope["url_route"])
            self.user_main = KinoUsers.objects.get(username=self.scope["url_route"]["kwargs"]["сlientname"])
        
        
        self.chat, created = Chat.objects.get_or_create(user_main=self.user_main, user_support=self.user_support)
        self.group_name = self.user_main.username + self.user_support.username
        
        return self.chat.id
    
    @database_sync_to_async
    def create_message(self, user, content, chat):
        Message.objects.create(user=user, content=content, chat=chat)
        
    async def receive(self, text_data):
        print("receive")
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.create_message(self.user, message, self.chat)
        await self.channel_layer.group_send(
            self.group_name, {"type":"send_message_users", "text":message, "from_who":self.user__username}
        )
    
    
    
    async def send_message_users(self, event):
        print("send")
        text= event["text"]
        from_who = event["from_who"]
        await self.send(text_data=json.dumps({"text":text, "from_who": from_who}))
        
        
        
        
        
        
        
    