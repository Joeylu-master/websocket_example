from asgiref.sync import async_to_sync
from django.db import models
from model_utils import FieldTracker




class Foo(models.Model):
    tracker = FieldTracker(fields=("bar",))
    bar = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        ret = super().save(*args, **kwargs)
        has_changed = self.tracker.has_changed("bar")
        if has_changed:
            # This is the wrapper that lets you call an async
            # function from inside a synchronous context:
            async_to_sync(update_foo)(self)
        return ret


from channels.layers import get_channel_layer
from .serializers import FooSerializer

async def update_foo(foo):
    serializer = FooSerializer(foo)
    group_name = serializer.get_group_name()
    channel_layer = get_channel_layer()
    content = {
        # This "type" passes through to the front-end to facilitate
        # our Redux events.
        "type": "UPDATE_FOO",
        "payload": serializer.data,
    }
    await channel_layer.group_send(group_name, {
        # This "type" defines which handler on the Consumer gets
        # called.
        "type": "notify",
        "content": content,
    })