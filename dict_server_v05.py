"""
服务端 v5.0
使用多进程tcp并发
1. 创建套接字对象
2. 设置端口重用
3. 绑定端口
4. 进行监听处理 listen
5. 循环接收连接的请求 accept
6. 处理客户端发送的注册请求
7. 处理客户端发送的登录请求
8. 处理查询单词的请求
9. 处理查询历史记录的请求
10. 处理客户端的退出请求
"""
from socket import *
from multiprocessing import Process
from dict_db import Database
from time import sleep
import sys

HOST = "127.0.0.1"
PORT = 12306
ADDR = (HOST, PORT)
db = Database()


def handle(c):
    while True:
        data = c.recv(1024).decode()
        if data[0] == "E" or data is None:
            # 处理客户端请求的子进程退出
            sys.exit(str(c.getpeername()[0])+"已经退出～")
        if data[0] == "R":  # 处理注册请求
            do_register(c, data)
        elif data[0] == "L":  # 处理登录请求
            do_login(c, data)
        elif data[0] == "Q":  # 处理查询单词的请求
            do_query(c, data)
        elif data[0] == "H":
            # s：服务端的套接字对象 c: 服务端与客户端之间的连接套接字对象
            do_history(c, data)


def do_history(c, data):
    """
    1. 解析数据，获取查询的用户名
    2. 查询数据库 -> history
    3. 将数据返回给客户端，注意粘包 sleep()
    [
        [1, zhangsan, hello]
        [1, zhangsan, hello]
        [1, zhangsan, hello]
        [1, zhangsan, hello]
    ]
    :param c:
    :param data:
    :return:
    """
    username = data.split(" ")[1]
    #  在数据库中查询历史记录
    result = db.select_history(username)
    for temp in result:
        # ('zhangsan', 'low', datetime.datetime(2020, 6, 6, 20, 7, 1))
        msg = "用户名:%s, 查询的单词记录: %s, 查询的时间: %s" % temp
        sleep(0.1)
        c.send(msg.encode())
    sleep(0.1)  # 避免发送给客户端的最后一条历史记录与结束符发生粘包现象
    c.send("##".encode())


def do_query(c, data):
    """
    1. 处理客户端发来的请求，解析数据，获得username和word
    2. 查询数据库
    3. 没查询一个单词，就要在历史记录表(history)中插入一条记录
    4. 给客户端发送响应
    Q nfx nice
    :param c:
    :param data:
    :return:
    """
    username = data.split(" ")[1]
    word = data.split(" ")[2]
    # 查询单词解释
    mean = db.query(word)
    # 增加历史记录
    db.insert_history(username, word)
    if mean:
        # nice: adj.decribe .....
        msg = "{}: {}".format(word, mean)
    else:
        msg = "该单词不在字典中，查询失败"
    c.send(msg.encode())


def do_login(c, data):
    """
    1. 处理客户端发来的请求，解析数据，获得username和password
    2. 查询数据库
    3. 给客户端发送响应
    :return:
    """
    # 1. 处理客户端发来的请求
    username = data.split(" ")[1]
    password = data.split(" ")[2]
    # 2. 查询数据库
    if db.login(username, password):
        c.send(b"OK")
    else:
        c.send(b"Fail")

def do_register(c, data):
    """
    查询user表中是否存在username
    :param c:
    :param data:
    :return:
    """
    # R nfx 123456  -> ["R", "nfx", "123456"]
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
















