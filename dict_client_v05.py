"""
客户端 v5.0
1. 与服务端建立连接
2. 给用户显示功能菜单
3. 给服务端发送注册请求
4. 给服务端发送登录请求
5. 发送查单词的请求
6. 查询历史记录
7. 退出功能
"""
from socket import *
from getpass import getpass
import sys

# 服务端地址
ADDR = ("127.0.0.1", 12306)

# 建立套接字对象，并与服务端建立连接
s = socket()
s.connect(ADDR)


def do_register():
    """
    注册逻辑：
        输入用户名
            用户名不能重复
                - 查询user表中是否存在username，存在则不合规则
            用户名当中不能含有特殊符号(空格......)
                - 获取到用户名之后，in
        输入密码
            密码当中不能含有特殊符号(空格......)
                - 获取到密码之后，in
        确认密码
            如果两次密码输入不正确，则注册失败
        向服务端发送注册的请求：以 R 开头的请求
    :return:
    """
    while True:
        username = input("请输入用户名：")
        password = getpass("请输入密码：")
        password_again = getpass("请再次输入密码：")

        if password != password_again:
            print("两次输入的密码不一致")
            continue

        if (" " in username) or (" " in password):
            print("用户名或密码中有特殊符号")
            continue

        # 向服务端发送请求
        msg = "R {} {}".format(username, password)
        s.send(msg.encode())
        data = s.recv(1028).decode()
        if data == "OK":
            print("注册成功")
        else:
            print("注册失败")
        break

def do_query(username):
    """
    1. 用户输入要查询的单词
    2. 将请求发送给服务端  "Q username word"
    3. 接收服务端的响应
    4. 显示查询结果
    :param username:
    :return:
    """
    while True:
        word = input("请输入要查询的单词：")
        if word == "##":  # 查询结束
            break
        msg = "Q {} {}".format(username, word)
        s.send(msg.encode())
        # data所对应的信息是单词的解释或者查询失败的消息
        data = s.recv(1024).decode()
        print(data)



def login(username):
    """
    二级界面
    :param username:
    :return:
    """
    while True:
        print("功能列表： 1.查单词  2.查询历史记录  3.注销")
        cmd = input("请选择功能: ")
        if cmd == "1":
            do_query(username)
        elif cmd == "2":
            do_history(username)
        elif cmd == "3":
            # return则表示二级界面以及他的所有功能执行结束
            # 会跳转到1级界面，选择登录，注册，或者退出的功能
            return
        else:
            print("请重新选择～")

# 查询历史记录(默认返回最近的5条数据)
def do_history(username):
    msg = "H {}".format(username)
    s.send(msg.encode())
    # 循环接收服务端的响应(历史记录)
    while True:
        data = s.recv(1024).decode()
        if data == "##":  # 如果服务端响应的数据为##,则表示数据发送完毕
            break
        print(data)

# 发送登录的请求
def do_login():
    """
    1. 输入用户名和密码
    2. 给服务端发送登录的请求  "L username password"
    :return:
    """
    username = input("请输入用户名：")
    password = getpass("请输入密码：")
    msg = "L {} {}".format(username, password)
    s.send(msg.encode())  # 发送请求
    data = s.recv(1024).decode()
    if data == "OK":
        print("登陆成功")
        # 如果登录成功，则给用户展示二级界面
        login(username)
    else:
        print("登录失败")


def main():  # 处理客户端的主逻辑
    while True:
        print("欢迎您： 1.注册  2.登录  3.退出")
        cmd = input("请选择功能(输入序号，并回车即可～)")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            do_login()
        elif cmd == "3":
            # 客户端给服务端发送退出的请求 E 表示退出的请求
            s.send(b"E")
            # 同时该进程结束
            sys.exit("欢迎下次再来～")
        else:
            print("请输入正确的序号～")


if __name__ == '__main__':
    main()


