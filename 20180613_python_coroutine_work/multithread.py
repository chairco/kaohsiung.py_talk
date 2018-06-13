#-*- coding: utf-8 -*-
import socket
import time
import concurrent.futures


URLS = ['/foo', '/bar']


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


start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    future_to_url = {executor.submit(get, url): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
    
    print('multithreading took %.1f sec' % (time.time() - start))

