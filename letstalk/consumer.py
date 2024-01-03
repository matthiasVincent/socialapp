from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import ChatInbox, Messages
from django.contrib.auth import get_user_model
from .serializers import MessageSerializer
from django.db.models import Q

User = get_user_model()

class NewChatConsumer(WebsocketConsumer):
    
    def connect(self):
        print("I am connected!")
        self.room_name = self.scope["url_route"]["kwargs"]["query"]
        self.auth_user = self.scope['user']
        #self.user = self.scope['user']
        #if not user.is_authenticated:
        #    return
        self.friend = self.room_name.split("_")[0]
        self.friend_user = User.objects.get(username=self.friend)
        print(self.room_name, self.auth_user, self.friend)
        self.new_group = "chat_{}".format(self.room_name)
        self.syn_group = "chat_{}_{}".format(self.auth_user, self.friend)
        #print(self.new_group, self.syn_group)
        prev_msgs = Messages.objects.filter(
            Q(sender=self.auth_user, receiver=self.friend_user)|
            Q(sender=self.friend_user, receiver=self.auth_user)).order_by('created').all().reverse()[:10]
        print(prev_msgs)
        self.chat, created = ChatInbox.objects.get_or_create(name=self.new_group)
        async_to_sync(self.channel_layer.group_add)(
            self.new_group, self.channel_name
        )
        self.accept()
        # self.send(json.dumps( 
        #     {
        #         "type": "welcome_message",
        #         "message": "Hey buddy, I am new consumer...you are connected succsfully!"
        #     })
        # )
        self.send(json.dumps( 
            {
                "type": "previous_message",
                "message": MessageSerializer(prev_msgs, many=True).data
            })
        )
    
    def disconnect(self, code):
        print("You are disconnected!")
        async_to_sync(self.channel_layer.group_discard)(self.new_group, self.channel_name)
        return super().disconnect(code)
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        message = text_data_json["message"]
        if message_type == "chat_message":
            message = Messages.objects.create(
                room_name=self.chat,
                sender = self.auth_user,
                receiver = self.friend_user,
                text_message = message
            )
        #print(MessageSerializer(message).data)
        async_to_sync(self.channel_layer.group_send)(
            self.new_group,
            {
                "type": "chat.message",
                "message": MessageSerializer(message).data
            } 
        )
        async_to_sync(self.channel_layer.group_send)(
            self.syn_group,
            {
                "type": "chat.message",
                "message": MessageSerializer(message).data
            } 
        )
    
    def chat_message(self, event):
        print(event["message"])
        message = event["message"]
        self.send(json.dumps(
            {
                "type": "chat_message",
                "message": message
            }
        ))