import socket
import time

from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ


selector = DefaultSelector()

n_jobs = 0

start = time.time()


class Future:
    def __init__(self):
        self.callbacks = []

    def resolve(self):
        for fn in self.callbacks:
            fn()


class Task:
    def __init__(self, coro):
        self.coro = coro
        self.step()

    def step(self):
        try:
            future = next(self.coro)
        except StopIteration:
            return
        future.callbacks.append(self.step)


def get(path):
    global n_jobs
    n_jobs += 1
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    f = Future()
    selector.register(s.fileno(), EVENT_WRITE, f)
    yield f
    selector.unregister(s.fileno())

    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    buf = []

    while True:
        f = Future()
        selector.register(s.fileno(), EVENT_READ, f)
        yield f
        selector.unregister(s.fileno())

        chunk = s.recv(1000)
        if chunk:
            buf.append(chunk)
        else:
            body = b''.join(buf).decode()
            print(body.split('\n')[0])
            n_jobs -= 1
            return 


Task(get('/foo'))
Task(get('/bar'))

while n_jobs:
    events = selector.select()
    for key, mask in events:
        future = key.data
        future.resolve()


print('%.2f secondes' % (time.time() - start))

