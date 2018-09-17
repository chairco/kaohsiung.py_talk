#-*- coding: utf-8 -*-
import asyncio
import random
import time
import os
os.environ['PYTHONASYNCIODEBUG'] = '1'

async def gen(num):
    i = 0
    while True:
        yield i
        i += 1
        if i == num:
            break
        # time.sleep(0.5)
        if i == 3:
            print('sleep 5s')
            await asyncio.sleep(5) # async sleep
            print('end sleep')


async def produce(queue, n):
    start = time.time()
    async for x in gen(n + 1):
        item = str(x)
        # produce an item
        print(f"producing {item}/{n}, id:{id(item)}")
        # simulate i/o operation using sleep
        await asyncio.sleep(random.random())
        # put the item in the queue
        await queue.put(item)


async def consume(queue):
    while True:
        # wait for an item from the producer
        item = await queue.get()

        # process the item
        print(f"consuming {item}..., id:{id(item)}")
        # simulate i/o operation using sleep
        await asyncio.sleep(random.random())

        # Notify the queue that the item has been processed
        queue.task_done()



async def run(n):
    queue = asyncio.Queue()
    # schedule the consumer
    consumer = asyncio.ensure_future(consume(queue))
    # run the producer and wait for completion
    await produce(queue, n)
    # wait until the consumer has processed all items
    await queue.join()
    # the consumer is still awaiting for an item, cancel it
    consumer.cancel()


loop = asyncio.get_event_loop()
loop.run_until_complete(run(5))
loop.close()