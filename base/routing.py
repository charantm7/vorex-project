from django.urls import re_path
from . import consumer

websocket_urlpatterns = [
    re_path(r'ws/group_chat/(?P<room_name>\w+)/$', consumer.GroupChatConsumer.as_asgi()),
]
