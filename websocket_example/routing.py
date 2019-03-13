from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from chat import consumers, routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # 普通的HTTP请求不需要我们手动在这里添加，框架会自动加载过来
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})