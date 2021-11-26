from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/product_counts/', consumers.ProductCountConsumer.as_asgi()),
    re_path(r'ws/chat/', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/jokes/', consumers.JokesConsumer.as_asgi()),
    re_path(r'ws/story/', consumers.StoryConsumer.as_asgi()),
    re_path(r'ws/last_updates/', consumers.LastUpdatesConsumer.as_asgi()),
]
