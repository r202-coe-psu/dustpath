import asyncio
import os
import logging
from nats.aio.client import Client as NATS


async def listen_nats(message_queue: asyncio.Queue):
    # Connection to NATS message queue
    # nats_url = os.getenv("NATS_URL", "nats://nats:4222")
    nc = NATS()
    await nc.connect("localhost:4222")

    async def message_handler(msg):
        data = msg.data.decode()
        logging.debug("handling new message: {}".format(data))
        await message_queue.put(data)

    # Subscription to all data related messages
    await nc.subscribe("home", cb=message_handler)

    # TODO: figure out how to close the NATS connection?


async def main():
    print("----->1")
    stop_signal = asyncio.Event()
    message_queue = asyncio.Queue()
    ts_task = asyncio.create_task(listen_nats(message_queue))
    print("----->2")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        stop_signal.set()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    asyncio.run(main())