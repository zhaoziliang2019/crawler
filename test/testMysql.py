import pymysql

# 连接到MySQL数据库
conn = pymysql.connect(
    host='localhost',  # MySQL服务器地址
    user='root',  # 用户名
    password='root',  # 密码
    database='test.db',  # 数据库名称
    charset='utf8mb4'  # 字符编码
)
# 创建数据库游标
cursor = conn.cursor()

# 创建表的SQL语句
create_table_query = """
CREATE TABLE IF NOT EXISTS employees (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  age INT,
  salary DECIMAL(10, 2)
)
"""

# 执行创建表的SQL语句
cursor.execute(create_table_query)
cursor.commit()
# 关闭游标和数据库连接
cursor.close()
conn.close()