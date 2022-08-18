import asyncio
from time import sleep
from urllib import request
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout
import time

class ControllerServer:
    def __init__(self):
        self.nc = NATS()

    async def message_handler(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    async def help_request(self, msg):
        print(f"Received a message on '{msg.subject} {msg.reply}': {msg.data.decode()}")
        await self.nc.publish(msg.reply, b'I can help')

    async def request_msg(self, msg):
        try:
            print("------>5")
            response = await self.js.request("foo", b'help me', timeout=0.5)
            print("Received response: {message}".format(
                message=response.data.decode()))
            print("------>6")
        except TimeoutError:
            print("Request timed out")
    
    async def setup(self):
        await self.nc.connect("localhost:4222")
        self.js = self.nc.jetstream()
        await self.js.add_stream(name="sample-stream", subjects=["foo"])
        psub = await self.js.pull_subscribe("foo", "psub")
        # for i in range(0, 10):
        #     ack = await self.js.publish("foo", f"hello world: {i}".encode())
        #     print(ack)
        print("------>2")
        sub = await self.js.subscribe("foo")
        msg = await sub.next_msg()
        await msg.ack()
        # sub1 = await self.nc.subscribe("foo", cb=self.message_handler)
        print("------>3")
        # sub2 = await self.nc.subscribe("help", "workers", cb=self.help_request)


    def run(self):
        # loop = asyncio.new_event_loop()
        print("------>1")
        asyncio.run(self.setup())
        asyncio.run(self.request_msg("---->4"))
        # asyncio.set_event_loop(loop)
        # try:
        #     loop.run_forever()
        # except Exception as e:
        #     print(e)
        # finally:
        #     loop.close()

x = ControllerServer()
x.run()