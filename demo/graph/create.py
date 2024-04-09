import json
import random
import math
import pandas as pd
from ...algorithm.A_start.grid.srccode import *
from ...algorithm.A_start.graph.srccode import *

# config配置
from test.config.test_fonig import *
def parse_pd_graph(json_file,start,end):
    data = pd.read_json(json_file)
    newdata = data.values
    # graph = NetworkXCompatibleGraph()
    graph = Graph()
    nodes = []
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
            else:
                pass
    return graph