from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import socket
import time


selector = DefaultSelector()
n_jobs = 0


##### evnet loop #####
def get_eventloop(path):
    global n_jobs
    n_jobs += 1
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    callback = lambda: connected_event(s, path)  # closure
    # non-blocking sockets
    selector.register(s.fileno(), EVENT_WRITE, data=callback)


def connected_event(s, path):
    selector.unregister(s.fileno())
    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    callback = lambda: readable_event(s, chunks)
    # non-blocking sockets
    selector.register(s.fileno(), EVENT_READ, data=callback)


def readable_event(s, chunks):
    global n_jobs
    selector.unregister(s.fileno())
    chunk = s.recv(1000)
    if chunk:
        chunks.append(chunk)
        callback = lambda: readable_event(s, chunks)
        # non-blocking sockets
        selector.register(s.fileno(), EVENT_READ, data=callback)
    else:
        body = (b''.join(chunks)).decode()
        print(body.split('\n')[0])
        n_jobs -= 1


##### aync callbacks #####
def get_callback(path):
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    callback = lambda: connected(s, path)
    selector.register(s.fileno(), EVENT_WRITE)
    selector.select()
    callback()


def connected(s, path):
    selector.unregister(s.fileno())
    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    callback = lambda: readable(s, chunks)
    selector.register(s.fileno(), EVENT_READ)
    selector.select()
    callback()


def readable(s, chunks):
    selector.unregister(s.fileno())
    chunk = s.recv(1000)
    if chunk:
        chunks.append(chunk)
        callback = lambda: readable(s, chunks)
        selector.register(s.fileno(), EVENT_READ)
        selector.select()
        callback()
    else:
        body = (b''.join(chunks)).decode()
        print(body.split('\n')[0])
        return


##### aync non-bocking ######
def get_non_blocking(path):
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    # non-blocking sockets
    selector.register(s.fileno(), EVENT_WRITE)
    selector.select()
    selector.unregister(s.fileno())

    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    while True:
        # non-blocking sockets
        selector.register(s.fileno(), EVENT_READ)
        selector.select()
        selector.unregister(s.fileno())

        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            body = (b''.join(chunks)).decode()
            print(body.split('\n')[0])
            return


##### sync #####
def get(path):
    s = socket.socket()
    s.connect(('localhost', 5000))
    request = 'GET %s HTTP/1.0\r\n\r\n' % path
    s.send(request.encode())

    chunks = []
    while True:
        chunk = s.recv(1000)
        if chunk:
            chunks.append(chunk)
        else:
            body = (b''.join(chunks)).decode()
            print(body.split('\n')[0])
            return


class GET:

    def __init__(self):
        self.start = time.time()
        global n_jobs
        global c_n_jobs

    @property
    def sync(self):
        get('/foo')
        get('/bar')
        return('sync took %.1f sec' % (time.time() - self.start))

    @property
    def nonblocking(self):
        get_non_blocking('/foo')
        get_non_blocking('/bar')
        return('non-blocking took %.1f sec' % (time.time() - self.start))

    @property
    def callback(self):
        get_callback('/foo')
        get_callback('/bar')
        return('callback took %.1f sec' % (time.time() - self.start))

    @property
    def eventloop(self):
        get_eventloop('/foo')
        get_eventloop('/bar')

        while n_jobs:
            #print('%d, took %.1f sec' % (n_jobs, time.time() - self.start))
            events = selector.select()
            # what next?
            for key, mask in events:
                cb = key.data
                cb()
        return('event_loop took %.1f sec' % (time.time() - self.start))



if __name__ == '__main__':
    g = GET()
    #print(g.sync)
    #print(g.nonblocking)
    #print(g.callback)
    print(g.eventloop)