# encoding:utf-8
__author__ = 'xyc'

import socket
import select
import sys

def ds_aynocore(addr, callback, timeout=5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    r, w, e = select.select([s], [], [], timeout)
    if r:
        response_data = s.recv(1024)
        callback(response_data)
        s.close()
        return 0
    else:
        s.close()
        return 1

if __name__ == "__main__":

    def callback(response_data):
        print response_data

    ds_aynocore(('127.0.0.1', 33333), callback, timeout=5)
