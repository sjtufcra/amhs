# 测试数据的起点/终点
start_point = 120
end_point = 1234

# json邻域文件地址
jsonPath = "./data/adjacent_matrix_test1.json"

# 数据库信息
dbname ='astart'
tablename ='graph'
key_join = ['id int AUTO_INCREMENT PRIMARY KEY', 'node json', 'edge json']

# 服务器地址
server_url = "http://0.0.0.0:8099/send/json/"