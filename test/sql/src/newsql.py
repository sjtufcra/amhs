import pymysql

# 创建数据  
def create_database(youname,database):
        # 连接参数
    # host = 'localhost'  # MySQL服务器的IP或主机名
    # port = 3306         # MySQL服务器的端口（默认为3306）
    user = youname # MySQL用户的用户名
    password = 'Zhang7262574.'  # MySQL用户的密码

    # 创建连接（无需指定数据库，因为此时要创建新数据库）
    connection = pymysql.connect(user=user, password=password)

    try:
        # 创建游标对象
        cursor = connection.cursor()

        # 定义要创建的新数据库名称
        new_db_name = database

        # 编写创建数据库的SQL语句
        create_db_query = f"CREATE DATABASE {new_db_name}"

        # 执行创建数据库的操作
        cursor.execute(create_db_query)

        print(f"Database '{new_db_name}' has been created successfully.")

    finally:
        # 关闭游标和连接（确保资源释放，即使出现异常）
        cursor.close()
        connection.close()

def connect_to_database(db_name):
    try:
        # 连接到数据库
        connection = pymysql.connect(
            user='root',
            password='Zhang7262574.',
            db=db_name,
            charset='utf8mb4'
        )
        return connection
    except:
        print("连接数据库失败")
# 创建数据表
def create_table(db_name, table_name, columns):
    try:
        connection = connect_to_database(db_name)
        cursor = connection.cursor()
        create_table_query = f"CREATE TABLE {table_name} ({','.join(columns)})"
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{table_name}' created successfully.")
        connection.close()
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False