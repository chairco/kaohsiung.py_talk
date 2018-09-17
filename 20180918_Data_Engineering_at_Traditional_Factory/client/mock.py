#-*- coding: utf-8 -*-
import asyncio
import aiohttp
import alog
import json
import random
import signal
import serial_asyncio
import time
import click

from datetime import datetime


# server setting
ip = "localhost:8000"
url_boards = f"http://{ip}/boards/records/"

# serial setting
com = '/dev/cu.usbmodem1411'
port = 9600

# data format
len_map = ['pink', 'orange', 'yellow', 'green', 'blue']
rs232_len = 16


def filter(received):
    """
    filter data content
    """
    datas = received.split(',')
    rs232_time = f"{','.join(datas[0:2])}"
    num = datas[2]
    machine = datas[3]
    datas = [float(m) for m in datas[4:6]]
    record_dict = {
        'rs232_time': rs232_time,
        'num': num,
        'machine': machine,
        'datas': datas
    }
    return record_dict


def record_data(data):
    """
    Create film data format by fake_msg()
    """
    datas = {f'measure_{idx+1}': value for idx, value in enumerate(data['datas'])}
    # create rs232 time
    rs232 = datetime.strptime(data['rs232_time'],'%y/%m/%d,%H:%M:%S')
    payload = {
        'num': data['num'],
        'machine': data['machine'],
        'rs232_time': rs232.strftime("%Y-%m-%dT%H:%M:%S"),
        'record_datas': datas
    }
    return payload


def fake_msg(i):
    """
    Simulation data
    """
    ret = random.randint(1, 2)
    msg = (f"{datetime.now().strftime('%y/%m/%d,%H:%M:%S')}, {i}, {ret},"
           f"{round(random.uniform(1.5,2), 3)},{round(random.uniform(1.8,2.5), 3)},")
    return msg


async def pv200(num, fake_msg):
    """
    Get the fake rs232 data
    :param num: number how many fake data
    :return: yield a string of rs232 records, but it's block
    """
    i = 0
    while True:
        yield fake_msg(i)
        i += 1
        if i == num:
            break
        await asyncio.sleep(5)



async def async_records(session, url, payload):
    """
    Async post data into server
    :param session
    :param url
    :param payload
    :return status, resp
    """
    async with session.post(url, json=payload) as resp:
        return resp.status, await resp.json()


async def async_post(session, url_boards, data):
    """
    Async flow to get id and post rs232 data into server
    :param session
    :param url_seq
    :param url_boards
    :param data
    """
    try:
        # Todo if post films fail should be delete seqid
        d = filter(data)
        payload = record_data(data=d)
        # post films
        status, films = await async_records(session, url_boards, payload=json.dumps(payload))
        return status, films

    except Exception as e:
        return False, str(e)


async def produce_rs232(queue, n=None, **kwargs):
    """
    Creat the real rs232 data into queue, is non-blocking
    :param queue
    :param n
    :param **kwargs
    """
    reader, writer = await serial_asyncio.open_serial_connection(url=com, **kwargs)
    buffers = ''
    index = 0
    while True:
        data = await reader.readline()
        buffers += data.decode('utf-8')
        alog.info(buffers)
        buf = buffers.split('\r')[-2].split(',')
        if len(buf) < rs232_len:
            alog.info(f"Drop not illeage {len(buf)}")
            buffers = ''
        elif '\r' in buffers:
            buf = buffers.split('\r')
            last_received, buffers = buffers.split('\r')[-2:]
            buffers = buffers.strip() # clean \n
            alog.info(f"producing {index}/{n}, id:{id(last_received)}, {last_received.split(',')[2]}")
            index += 1
            await asyncio.sleep(random.random())
            await queue.put(last_received)


async def produce(loop, queue, n, fake_msg):
    """
    Create fake rs232 data into queue, it's blocking
    :param queue
    :param n
    """
    index = 0
    try:
        async for data in pv200(n, fake_msg):
            # produce rs232 data
            alog.info(f"producing {index}/{n}, id:{id(data)}, {data.split(',')[2]}")
            index += 1
            # simulate i/o operation data
            await asyncio.sleep(random.random())
            # put into list
            await queue.put(data)
    except Exception as e:
        alog.info(e)


async def consume(queue):
    """
    Post rs232 data into server
    :param queue
    """
    async with aiohttp.ClientSession() as session:
        try:
            while True:
                # wait for an data from producer
                data = await queue.get()
                # process the item
                alog.info(f"consuming id:{id(data)}")
                status, result = await async_post(session, url_boards, data)
                if status != 201:
                    alog.error(f"error: id:{id(data)}, {status}, {result}")
                    await queue.put(data)
                # simulate i/o operation using sleep
                await asyncio.sleep(random.random())
                # Notify the queue that the item has been processed
                queue.task_done()
        except Exception as e:
            alog.info(f"Finish: {e}.")


async def run(loop, n, fake_msg, fake=True):
    """
    mock server main function, create async queue and put it into a ensure_future()
    :param n
    :param fake_msg
    """
    queue = asyncio.Queue()
    # schedule the consumer
    consumer = asyncio.ensure_future(consume(queue))
    # run the producer and wait for completion(rs232 mode, and gen mode)
    if fake:
        await produce(loop, queue, n, fake_msg)
    else:
        await produce_rs232(queue, n, baudrate=port, timeout=0, dsrdtr=True, rtscts=True)
    # wait until the consumer has processed all items
    await queue.join()
    # the consumer is still awaiting for an item, cancel it
    consumer.cancel()


@click.command()
@click.option('--device', default='/dev/cu.usbmodem1411', help="device's com.")
@click.option('--port', default=9600, help="device's port.")
@click.option('--server', default='localhost', help="restful server address.")
@click.option('--num', default=None, type=int, help="execute times.")
@click.option('--fake', default=True, help="Selet really env.")
def main(device, port, server, num, fake):
    """
    create asyncio event loop
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop, num, fake_msg, fake))
    loop.close()


if __name__ == '__main__':
    main()

