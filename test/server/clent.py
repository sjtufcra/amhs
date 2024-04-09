from fastapi import FastAPI
import pymysql

app = FastAPI()

# 获取节点数据
@app.get("/getNode/")
def getNode():
    node = slecet_table()[0]
    return node
# 获取边数据
@app.get("/getEdge/")
def getEdge():
    edg = slecet_table()[1]
    return edg

@app.get("/getGraph/")
def getGraph():
    data = slecet_table()
    return data
# 默认结果
@app.get("/")
def read_root():
    return {"Hello": "World"}





# 数据库操作

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

def slecet_table():
    name = 'graph'
    db = connect_to_database('astart')
    try:
        cursor = db.cursor()
        query = "SELECT * FROM " + name
        cursor.execute(query)

        # 获取查询结果
        result = cursor.fetchall()

        # 将查询结果转换为列表的列表（便于后续处理或直接返回）
        rows = [list(row) for row in result]

        return rows

    finally:
        cursor.close()
        db.close()
# 初始化
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)