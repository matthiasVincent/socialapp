"""
ASGI config for chan_projs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import URLRouter
from letstalk.routing import websocketpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chan_projs.settings')

django_app = get_asgi_application()
import letstalk.routing

application = ProtocolTypeRouter(
    {
        "http": django_app,
        "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(
            URLRouter(websocketpatterns),
        ))
    }
)