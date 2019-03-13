from django.urls import path

from chat import consumers

websocket_urlpatterns = [ # 路由，指定 websocket 链接对应的 consumer
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer),
]
