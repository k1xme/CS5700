import html
import xml
import socket
import sys
import select


class Worker(object):
    """
    Worker wraps a TCP socket and its current reading, writing states.
    This class is designed for supporting asynchronous pattern.
    """
    def __init__(self, s=None):
        self.socket = s or socket.socket()
        self.socket.setblocking(0)
        self.read_buf = ''
        self.write_buf = ''
        self.read_pos = 0
        self.write_pos = 0

    def read(self):
        pass

    def write(self, buf):
        pass

    def connect(self, host, port):
        pass

    def _on_write_done(self):
        pass

    def _on_read_done(self):
        pass

    def fileno(self):
        return self.socket.f-ileno()


class Crawler(object):
    """docstring for Crawler"""
    def __init__(self, user, passwd, conn_num=100):
        self.cookie = self.login(user, passwd)
        self.rlist, self.wlist, self.xlist = [], [], []
        self.flags = set()
        self.frointer = []
        self.visited = set()


    
    def start(self):
        while True:
            readables, writables, _ = select.select(rlist, wlist, xlist, 2)

            if readables: process_read(readables)
            if writables: process_write(writables)


    def make_http_req(self, headers, body={}):
        pass


    def get(self, url):
        pass


    def post(self, url, body):
        pass

    
    def extract_links(self, page):
        pass

    
    def find_secret_flag(self, page):
        pass

    
    def login(self, user, passwd):
        cookie = ''
        s = socket.socket()
        response = self.post('', body={})

        return cookie


if __name__ == '__main__':
    pass