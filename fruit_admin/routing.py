from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'product_counts/', consumers.ProductCountConsumer.as_asgi()),
    re_path(r'chat/', consumers.ChatConsumer.as_asgi()),
    re_path(r'jokes/', consumers.JokesConsumer.as_asgi()),
]
