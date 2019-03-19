import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # 当 websocket 一链接上以后触发该甘薯
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # 把当前链接添加到聊天室
        # 注意 `group_add` 只支持异步调用，所以这里需要使用`async_to_sync`转换为同步调用
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # 接受该链接
        self.accept()

    def disconnect(self, close_code):
        # 断开链接是触发该函数
        # 将该链接移出聊天室
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # 前端发送来消息时，通过这个接口传递
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 发送消息到当前聊天室
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                # 这里的type要在当前类中实现一个相应的函数，
                # 下划线或者'.'的都会被Channels转换为下划线处理，
                # 所以这里写 'chat.message'也没问题
                'type': 'chat.message',
                'message': message,
                'id':1
                # 'status': False
            }
        )

    # 从聊天室拿到消息，后直接将消息返回回去
    def chat_message(self, event):
        # message = event['message']
        message=True

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'status' : False
        }))