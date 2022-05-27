"""
ASGI config for DoorStepFarmer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DoorStepFarmer.settings')
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from Product.Consumer import MyConsumer


application = get_asgi_application()
websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', MyConsumer.as_asgi())
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns)
})