from fastapi import FastAPI,BackgroundTasks
import pymysql
import json

app = FastAPI()

@app.post('/send/json/')
def send_json(data:dict,bkt:BackgroundTasks):
    if data:
        bkt.add_task(update,data)
    return 'ok'

def update(data):
    if data is None:
        return
    node = data.get('nodes')
    edge = data.get('edges')
    name = data.get('tablename')
    slecet_table(name,node,edge)

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

def slecet_table(name,node,edge):
    if name is None:
        return
    db = connect_to_database('astart')
    cursor = db.cursor()
    create_table_query = f"INSERT INTO {name} (node,edge) VALUES ('{node}','{edge}');"
    cursor.execute(create_table_query)
    db.commit()
    print(f"Table '{name}' created successfully.")
    db.close()
    return True



if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8099)