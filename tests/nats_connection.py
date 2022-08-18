import asyncio
import nats
import json
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError

async def main():
    # It is very likely that the demo server will see traffic from clients other than yours.
    # To avoid this, start your own locally and modify the example to use it.

    nc = await nats.connect("localhost:4222")

    # async def message_handler(msg):
    #     subject = msg.subject
    #     reply = msg.reply
    #     data = msg.data.decode()
    #     print("Received a message on '{subject} {reply}': {data}".format(
    #         subject=subject, reply=reply, data=data))

    data = {
        'action': "register",
    }
    # response = await nc.request(
    #                     "dustpath.compute.report", json.dumps(data).encode(), timeout=10
    #                 )

    response = await nc.request(
                        "dustpath.storage.command", json.dumps(data).encode(), timeout=10
                    )
    
    # try:
    #     response = await nc.request("help", b'help me', timeout=0.5)
    #     print("Received response: {message}".format(
    #         message=response.data.decode()))
    # except TimeoutError:
    #     print("Request timed out")


if __name__ == '__main__':
    asyncio.run(main())
