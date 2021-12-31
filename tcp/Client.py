#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import socket
import time

HOST = '165.3.122.191'
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def sub_run_time(timetemp):
    start  = datetime.datetime.fromtimestamp(timetemp)
    run_time = datetime.datetime.now()-start
    return int(run_time.microseconds / 1000.0)

while True:
    date = str(time.time())
    print(date)
    s.send(date.encode())
    indata = s.recv(1024)
    print(str(sub_run_time(float(indata.decode())))+'ms')
    print(str(sub_run_time(float(indata.decode()))/2)+'ms')
    time.sleep(5)
    continue
    outdata = input('please input message: ')
    print('send: ' + outdata)
    s.send(outdata.encode())
    
    indata = s.recv(1024)
    if len(indata) == 0: # connection closed
        s.close()
        print('server closed connection.')
        break
    print('recv: ' + indata.decode())