import getpass
import hashlib  # 对密码进行散列算法处理

# 输入用户名和密码
username = input("请输入用户名：")
password = getpass.getpass("请输入密码：")
print("散列前", password)
salt = "abcde"  # 加盐处理
hash_md5 = hashlib.md5(salt.encode())  # 生成一个hash中的md5散列对象
hash_md5.update(password.encode())  # 对password进行md5散列算法处理
password = hash_md5.hexdigest()  # 获取散列后的值
print("散列后", password)
print("登陆成功～")


