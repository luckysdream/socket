#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import socket
import time,requests

HOST = '0.0.0.0'
PORT = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

def sub_run_time(timetemp):
    start  = datetime.datetime.fromtimestamp(timetemp)
    run_time = datetime.datetime.now()-start
    return int(run_time.microseconds / 1000.0)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

while True:
    conn, addr = s.accept()
    print('connected by ' + str(addr))

    while True:
        start  = datetime.datetime.now()
        indata = conn.recv(1024)
        print('到达时间:'+str(sub_run_time(float(indata.decode())))+'ms')
        print('到达时间/2:'+str(sub_run_time(float(indata.decode()))/2)+'ms')
        requests.get('http://www.gstatic.com/generate_204')
        conn.send(str(time.time()).encode())
        run_time = datetime.datetime.now()-start
        print('全程时间:'+str(int(run_time.microseconds / 1000.0))+'ms')
        #s.send(str(time.time()).encode())
        time.sleep(5)
        continue
        indata = conn.recv(1024)
        if len(indata) == 0: # connection closed
            conn.close()
            print('client closed connection.')
            break
        print('recv: ' + indata.decode())

        outdata = 'echo ' + indata.decode()
        conn.send(outdata.encode())