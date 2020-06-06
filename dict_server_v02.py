"""
服务端 v2.0
使用多进程tcp并发
1. 创建套接字对象
2. 设置端口重用
3. 绑定端口
4. 进行监听处理 listen
5. 循环接收连接的请求 accept
6. 处理客户端发送的注册请求
。。。。
"""
from socket import *
from multiprocessing import Process
from dict_db import Database

HOST = "127.0.0.1"
PORT = 12306
ADDR = (HOST, PORT)
db = Database()


def handle(c):
    while True:
        data = c.recv(1024).decode()
        if data[0] == "R":  # 处理注册请求
            do_register(c, data)


def do_register(c, data):
    """
    查询user表中是否存在username
    :param c:
    :param data:
    :return:
    """
    username = data.split(" ")[1]
    password = data.split(" ")[2]
    # 判断数据库中是否存在username的用户
    if db.register(username, password):
        c.send(b"OK")
    else:
        c.send(b"Fail")

def main():
    s = socket()  # 创建套接字对象
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 设置端口可重用
    s.bind(ADDR)  # 绑定地址
    s.listen(5)  # 监听
    print("正在监听12306端口......")

    while True:
        try:
            # 循环接收客户端的连接请求，是一个阻塞方法
            c, addr = s.accept()
            print("同客户端连接成功，地址为: {}".format(addr))
        except Exception as e:
            print(e)
            continue

        # 创建多进程去处理请求
        client = Process(target=handle, args=(c, ))
        client.daemon = True
        client.start()


if __name__ == '__main__':
    main()
















