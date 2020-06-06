"""
客户端 v2.0
1. 与服务端建立连接
2. 给用户显示功能菜单
3. 给服务端发送注册请求
"""
from socket import *
from getpass import getpass

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




def main():  # 处理客户端的主逻辑
    while True:
        print("欢迎您： 1.注册  2.登录  3.退出")
        cmd = input("请选择功能(输入序号，并回车即可～)")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            s.send("登录".encode())
        elif cmd == "3":
            s.send("退出".encode())
        else:
            print("请输入正确的序号～")


if __name__ == '__main__':
    main()


