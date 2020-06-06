"""
数据访问对象
向数据库发送指定的增删改查的请求
"""
import pymysql
import hashlib

# 加盐
salt = b"qwerdf"


# 密码散列化处理
# md5不是加密算法，是散列算法
def hash_password(password):
    hash = hashlib.md5(salt)
    hash.update(password.encode())
    return hash.hexdigest()  # 获取散列化处理后的密码


class Database:
    def __init__(self, host="127.0.0.1", port=3306,
                        user="root", password="123456",
                        database="dict", charset="utf8"):
        # 连接数据库
        self.db = pymysql.connect(host=host, port=port,
                        user=user, password=password,
                        database=database, charset=charset)

        # 建立游标对象：去执行sql语句的对象
        self.cur = self.db.cursor()

    def close(self):  # 关闭连接
        self.cur.close()
        self.db.close()

    def register(self, username, password):
        """
        1. 判断user表中是否存在用户名为username的字段
            - 存在，返回False
            - 不存在，则继续进行第二步
        2. 将该条用户信息存入到user表中
        :return:
        """
        # 1. 判断user表中是否存在用户名为username的字段
        sql = "SELECT * FROM user WHERE username = '%s'" % username
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            return False
        # 2. 将该条用户信息存入到user表中
        # 将密码进行散列化处理
        password = hash_password(password)
        try:
            sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
            self.cur.execute(sql, [username, password])
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    def login(self, username, password):
        """
        select * from user where username='nfx' and
            password = '123456';   ????
        :param username:
        :param password:
        :return:
        """
        password = hash_password(password)  # md5散列处理
        sql = "SELECT * FROM user WHERE username = %s and password = %s;"
        self.cur.execute(sql, [username, password])  # 执行sql语句
        result = self.cur.fetchone()  # 获取查询结果
        if result:  # 如果有返回值，则表示登陆成功
            return True
        else:
            return False

    def query(self, word):
        sql = "SELECT mean FROM words WHERE word='%s'" % word
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            # 返回的是单词的解释 mean
            return result[0]

    def insert_history(self, username, word):
        # 当用户查询完但此后执行此方法
        sql = "INSERT INTO history (username, word) VALUES (%s, %s);"
        try:
            self.cur.execute(sql, [username, word])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def select_history(self, username):
        sql = "SELECT username, word, time " \
              "FROM history " \
              "WHERE username = '%s' " \
              "ORDER BY time DESC " \
              "LIMIT 5" % username
        self.cur.execute(sql)
        return self.cur.fetchall()




