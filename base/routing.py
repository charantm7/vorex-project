from django.urls import path
from base.consumer import ChatConsumer  # Ensure this import exists

websocket_urlpatterns = [
    path("ws/chat/<str:chat_name>/", ChatConsumer.as_asgi()),
]