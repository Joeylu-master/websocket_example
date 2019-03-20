import pytest
from channels.testing import HttpCommunicator

from foo.consumers import NotificationConsumer
from foo.models import Foo, update_foo


@pytest.mark.asyncio
async def test_my_consumer():
    communicator = HttpCommunicator(NotificationConsumer, "GET", "/test/")
    response = await communicator.get_response()
    assert response["body"] == b"test response"
    assert response["status"] == 200
    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_json_to({
        "model": "as.Appropriate",
        "id": str(Foo.id),
    })
    assert await communicator.receive_nothing()

    await update_foo()
    response = await communicator.receive_json_from()
    assert response == {
        # ... whatever you expect
    }

    await communicator.disconnect()