from rest_framework import serializers
from .models import Messages
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username",]

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    #room_name = serializers.SerializerMethodField()

    class Meta:
        model = Messages
        fields = [
            "sender",
            "receiver",
            "text_message",
            "image_message",
            "created",
            "read",
        ]

    def get_sender(self, obj):
        return UserSerializer(obj.sender).data
    def get_receiver(self, obj):
        return UserSerializer(obj.receiver).data