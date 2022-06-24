import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class SNSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'msg': 'Connection accepted'
        }))

    def receive(self, text_data=None, bytes_data=None):
        meeting_id = json.loads(text_data)['meetingId']
        async_to_sync(self.channel_layer.group_add)(
            meeting_id,
            self.channel_name
        )

    def send_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
