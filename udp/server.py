import socket
import os
from time import sleep
import datetime

#建立 UDP Scoket
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#監聽 所有IP的 3386 端口 
listen_addr = ("0.0.0.0", 2333)
UDPSock.bind(listen_addr)
print("P2P Server in start")

#儲存IP用的 Array
ips = []

while True:
    #接收資料
    data, addr = UDPSock.recvfrom(1024)
    print (addr , 'is connected.')
    print(str(datetime.datetime.now()))
    #將Client IP:Port 儲存到Array內
    ips.append(str(addr[0]) + ':' + str(addr[1]))
    #當第二個Client連上時，進行IP交換動作
    if(len(ips) == 2):
        dest = ''
        for ip in ips:
            for i in ips:
                if ip != i:
                    dest = i # 對方的IP
                #將A的IP傳給B，B的IP傳給A
                if dest != '':
                    up = (ip.split(':')[0],int(ip.split(':')[1]))
                    UDPSock.sendto(bytes(dest.encode('utf-8')), up)
                    print("发送IP:")
                    print(up)
                    print("发送内容:")
                print(dest)
        print("即将清理内容!!!")
        sleep(5)
        os.system("cls")
        print("清除IP池")
        ips = []
    len(ips)
