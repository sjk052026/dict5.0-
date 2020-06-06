"""
客户端 v1.0
1. 与服务端建立连接
2. 给用户显示功能菜单
"""
from socket import *

# 服务端地址
ADDR = ("127.0.0.1", 12306)

# 建立套接字对象，并与服务端建立连接
s = socket()
s.connect(ADDR)


def main():  # 处理客户端的主逻辑
    while True:
        print("欢迎您： 1.注册  2.登录  3.退出")
        cmd = input("请选择功能(输入序号，并回车即可～)")
        if cmd == "1":
            s.send("注册".encode())
        elif cmd == "2":
            s.send("登录".encode())
        elif cmd == "3":
            s.send("退出".encode())
        else:
            print("请输入正确的序号～")


if __name__ == '__main__':
    main()


