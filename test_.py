import json
import random
import math
import pandas as pd
from algorithm.A_start.grid.srccode import *
from algorithm.A_start.graph.srccode import *
from test.chart.A_start_chart import *
from test.chart.A_start_graph import *
from test.server.requst import *
from test.sql.src.newsql import *
# config配置
from test.config.test_fonig import *
# 网格数据格式
def test_pd_grid(pd_file):
    data = pd.read_json(pd_file).values
    start_node = Node(0, 0)
    goal_node = Node(1289, 1892)

    # 生成网格
    grids = [[Node(x, y) for y in range(len(data[0]))] for x in range(len(data))]

    # 提取障碍物
    obstacles = {(x, y) for x, row in enumerate(data) for y, cell in enumerate(row) if cell == 0}

    # 计算最优路径
    path = a_star_search(
        start_node,
        goal_node,
        grids,
        obstacles
    )
    print(path)
# 图数据格式
def test_pd_graph(json_file,start,end):
    data = pd.read_json(json_file)
    newdata = data.values
    graph = NetworkXCompatibleGraph()
    nodes = []
    edgs = []
    print(data.axes[0][start], data.axes[0][end])
    # 生成图数据
    length = newdata.shape[0]
    flag = int(math.sqrt(length))+1
    row = 0
    col = 0
    for a in range(length):
        if a % flag !=0:
            row = row+1
        else:
            col = int(a/flag)*2
            row = 0
        node = Node(a, random.randint(1, 10),(col,row))
        nodes.append(node)
        graph.add_node(node)
    for x ,kin in enumerate(newdata):
        for y,key in enumerate(kin) :
            if key != 0:
                node1 = nodes[x]
                node2 = nodes[y]
                edg = Edge(start=node1,end=node2,weight = random.randint(1, 10))
                graph.add_edge(edg)
                edgs.append(edg)
            else:
                pass
    EdgJson = json.dumps(edgs,cls=EdgeEncoder)
    NodeJson = json.dumps(nodes,cls=NodeEncoder)

    # 临时导出
    # with open('./node.json', 'w', encoding='utf-8') as json_file:
    #     json_file.write(NodeJson)
    # with open('./edge.json', 'w', encoding='utf-8') as json_file:
    #     json_file.write(EdgJson)

    # 数据透传
    # jsdata = {
    #     "nodes":NodeJson,
    #     "edges":EdgJson,
    #     "tablename":tablename
    # }
    # # send_post(server_url,jsdata)
    return graph,nodes,start,end,data
    # 设定起始点
def computeLine(graph,nodes,start,end,data):
    graph.set_start_and_goal(nodes[start], nodes[end])
    # 绘制图
    # newgraph = graph.to_networkx_graph()
    # draw_graph(newgraph)

    try:
        astart = AStar()
        shortest_path_nodes = astart.a_star_search(graph)
        corrd = [node.coordinates for node in shortest_path_nodes]
        print(f"Shortest path nodes: {corrd}")
        print(f"Shortest path nodes: {[data.axes[0][node.coordinates[0]] for node in shortest_path_nodes]}")
        return corrd
    except ValueError as e:
        print(e)
# 测试
def test(json_file):
    # if not re.match(r'^[\w,\s-]+\.json$', json_file):
    #     print("非法的文件名或扩展名")
    #     return None

    try:
        with open(json_file) as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                print("JSON解析失败：文件格式可能不正确")
                return None
            except FileNotFoundError:
                print("文件不存在")
                return None
    except IsADirectoryError:
        print(f"{json_file}是一个目录，请指定一个有效的文件路径。")
        return None
# 解析固定数据的路径
def parse_data(json_data):
    data = test(json_data)
    if data:
        for x in data:
            for y,key in x :
                if y[key] != 0:
                    print(y)
            print(x)
        return data

# 示例：调用test函数并处理返回结果
# json_file_path = "./data/json/adjacent_matrix_test.json"  # 替换为实际的文件路径
json_file_path = jsonPath  # 替换为实际的文件路径
# test_pd_graph(json_file_path,start_point,end_point)
# create_table(dbname,tablename,key_join)

# 正常计算推理
result = computeLine(*test_pd_graph(json_file_path,start_point,end_point)) #数据来源
test_show(result)
if result:
    # 对返回的数据进行处理
    print(result)