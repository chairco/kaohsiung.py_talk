from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import socket
import time

selector = DefaultSelector()
n_jobs = 0

##### coroutines #####
class Future:

    def __init__(self):
        self.callbacks = None

    def resolve(self):
        self.callbacks()

    def __await__(self):
        yield self


class Task:

    def __init__(self, coro):
        self.coro = coro
        self.step()

    def step(self):
        try:
            f = self.coro.send(None)
        except StopIteration:
            return

        f.callbacks = self.step


async def get(path):
    global n_jobs
    n_jobs += 1
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    f = Future()
    selector.register(s.fileno(), EVENT_WRITE, data=f)
    await f
    # s is writable
    selector.unregister(s.fileno())
    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    buf = []
    while True:
        f = Future()
        # non-blocking sockets
        selector.register(s.fileno(), EVENT_READ, data=f)
        await f
        selector.unregister(s.fileno())
        chunk = s.recv(1000)
        if chunk:
            buf.append(chunk)
        else:
            break

    body = (b''.join(buf)).decode()
    print(body.split('\n')[0])
    n_jobs -= 1


start = time.time()

Task(get('/foo'))
Task(get('/bar'))

while n_jobs:
    events = selector.select()
    # what next?
    for key, mask in events:
        fut = key.data
        fut.resolve()
print('coroutines took %.1f sec' % (time.time() - start))