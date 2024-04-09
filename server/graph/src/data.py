import pandas as pd
import math
import random

# 自定义模块
from algorithm.A_start.graph.srccode import *

# 参数表
from server.config import *

class Data():
    def __init__(self) -> None:
        self.Graph = NetworkXCompatibleGraph()
        self.jsonfile = jsonPath
        self.read_pd_graph(self.jsonfile)
        pass
    
    def read_pd_graph(self,json_file):
        data = pd.read_json(json_file)
        newdata = data.values
        graph = self.Graph
        nodes = []
        edgs = []
        # 生成图数据
        length = newdata.shape[0]
        flag = int(math.sqrt(length))+1
        row = 0
        col = 0
        for a in range(length):
            h = random.randint(1, 10) #权重值默认随机值
            if a % flag !=0:
                row = row+1
            else:
                col = int(a/flag)*2
                row = 0
            node = Node(a, h ,(col,row))
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

        self.nodes = nodes
        self.edges = edgs
        self.data = data
        return
  