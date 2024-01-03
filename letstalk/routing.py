from django.urls import re_path, path
from . import consumer


websocketpatterns = [
    #re_path(r"ws/(?P<auth_user>)*/$", consumer.NewChatConsumer.as_asgi()),
    #re_path(r'/ws/[a-z][0-9]\+/$', consumer.NewChatConsumer.as_asgi()),
    path("ws/<str:query>/", consumer.NewChatConsumer.as_asgi()),
]