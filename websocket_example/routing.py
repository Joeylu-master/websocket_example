from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from chat import consumers
from foo.consumers import NotificationConsumer

websocket_urlpatterns = [  # 路由，指定 websocket 链接对应的 consumer
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer),
    path('ws/notifications/',NotificationConsumer,name='ws_notifications',
    ),
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # 普通的HTTP请求不需要我们手动在这里添加，框架会自动加载过来
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
