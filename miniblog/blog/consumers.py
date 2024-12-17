
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class BlogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the "posts" group
        await self.channel_layer.group_add(
            "posts",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the "posts" group
        await self.channel_layer.group_discard(
            "posts",
            self.channel_name
        )

    # Function to handle messages received from the WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = text_data_json.get('type')

        # Handle different event types
        if event_type == 'new_post':
            await self.handle_new_post(text_data_json)
        elif event_type == 'delete_post':
            await self.handle_delete_post(text_data_json)

        elif event_type == 'comment_message':
            await self.handle_comment_message(text_data_json)
        # Add more event types as needed

    # Function to handle 'new_post' event
    async def handle_new_post(self, data):
        await self.channel_layer.group_send(
            "posts",
            {
                'type': 'post_message',
                'title': data['title'],
                'description': data['description'],
                'id' : data['id']
            }
        )

    # Function to handle 'delete_post' event
    async def handle_delete_post(self, data):
        await self.channel_layer.group_send(
            "posts",
            {
                'type': 'delete_message',
                'id': data['id']
            }
        )

    
    # Function to handle 'post_message' event type
    async def post_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_post',
            'title': event['title'],
            'description': event['description']
        }))

    # Function to handle 'delete_message' event type
    async def delete_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'delete_post',
            'id': event['id']
        }))

    
    async def comment_message(self, event):
    
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'comment_message',
            'post_id': event['post_id'],
            'author': event['author'],
            'text':event['text'],
            'created_at':event['created_at']
        }))


    # Function to handle 'delete_post' event
    async def handle_comment_message(self, data):
        await self.channel_layer.group_send(
            "posts",
            {
                # 'type': 'comment_message',
                # 'id': data['id']

                'type': 'comment_message',
                'post_id': data['post_id'],
                'author': data['author'],
                'text':data['text'],
                'created_at':data['created_at']
            }
        )