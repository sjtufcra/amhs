import heapq 
import networkx as nx
from typing import Dict, List, Tuple

class Node:
    """
    图节点类，包含节点编号和坐标信息。
    """
    def __init__(self, id: int,h_scores: int, coordinates: Tuple[float, float]):
        self.id = id
        self.h = h_scores
        self.g = float('inf')
        self.f = float('inf')
        self.coordinates = coordinates
    def __lt__(self, other):
        return self.f < other.f

class Edge:
    """
    图边类，表示两个节点之间的连接，包含起始节点、结束节点和权重。
    """
    def __init__(self, start: Node, end: Node, weight: float):
        self.start = start
        self.end = end
        self.weight = weight

class Graph:
    """
    图类，采用邻接矩阵表示图结构，适用于 A* 算法。
    """
    def __init__(self):
        self.nodes: List[Node] = []
        self.edges: List[Edge] = []
        self.adjacency_matrix: Dict[Tuple[int, int], float] = {}

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        self.adjacency_matrix[(edge.start.id, edge.end.id)] = edge.weight
        # self.adjacency_matrix[(edge.end.id, edge.start.id)] = edge.weight  # 对于无向图，双向添加权重

    def get_neighbors(self, node_id: int) -> List[Tuple[Node, float]]:
        """
        获取指定节点的所有邻居节点及其对应的边权重。
        """
        neighbors = []
        for other_id, weight in self.adjacency_matrix.items():
            if other_id[0] == node_id:
                neighbor_id = other_id[1]
                neighbor = next((n for n in self.nodes if n.id == neighbor_id), None)
                if neighbor is not None:
                    neighbors.append((neighbor, weight))
        return neighbors

    def set_start_and_goal(self, start_node: Node, goal_node: Node):
        self.start_node = start_node
        self.goal_node = goal_node

class NetworkXCompatibleGraph(Graph):
    def __init__(self):
        super().__init__()
    def to_networkx_graph(self):
        """将当前图转换为networkx.Graph对象"""
        # G = nx.Graph() #无向图
        G = nx.DiGraph() #有向图

        # 添加节点
        for node in self.nodes:
            G.add_node(node.id, coordinates=node.coordinates)

        # 添加边
        for edge in self.edges:
            G.add_edge(edge.start.id, edge.end.id, weight=edge.weight)

        return G


class AStar:
    def __init__(self):
        pass
    def manhattan_distance(self,node, goal_node):
        """
        计算节点与目标节点之间的曼哈顿距离。
        """
        return abs(node.coordinates[0] - goal_node.coordinates[0]) + abs(node.coordinates[1] - goal_node.coordinates[1])
    def a_star_search(self,graph):
        """
        A* 算法实现，返回从起点到终点的最短路径节点序列。
        
        :param graph: 图对象，包含起点、终点和邻接关系。
        :return: 节点序列，从起点到终点的最短路径。
        """
        # 初始化开放列表，包含起点及其初始f值
        
        open_set = []
        heapq.heappush(open_set,(0, graph.start_node))
        # 记录每个节点的来源
        came_from = {graph.start_node.id: None}
        # 记录从起点到当前节点的代价
        g_scores = {graph.start_node.id: 0}
        # 记录当前节点到终点的估计代价
        # f_scores = {graph.start_node.id: self.manhattan_distance(graph.start_node, graph.goal_node)}
        f_scores = {graph.start_node.id: (g_scores[graph.start_node.id]+graph.start_node.h)}

        while open_set:
            # 从开放列表中选择f值最小的节点
            current_f_score, current_node = heapq.heappop(open_set)

            # 到达终点，路径查找结束
            if current_node == graph.goal_node:
                path = []
                # 逆向构建路径
                while current_node != graph.start_node:
                    path.append(current_node)
                    current_node = came_from[current_node.id]
                path.append(graph.start_node)
                path.reverse()
                return path

            # 遍历当前节点的邻居
            for neighbor, edge_weight in graph.get_neighbors(current_node.id):
                # 计算到达邻居节点的试探性代价
                tentative_g_score = g_scores[current_node.id] + edge_weight

                # 更新邻居节点的代价和路径信息
                if tentative_g_score < g_scores.get(neighbor.id, float('inf')):
                    came_from[neighbor.id] = current_node
                    g_scores[neighbor.id] = tentative_g_score
                    # f_scores[neighbor.id] = tentative_g_score + self.manhattan_distance(neighbor, graph.goal_node)
                    f_scores[neighbor.id] = tentative_g_score + neighbor.h
                    # 将邻居节点加入开放列表
                    heapq.heappush(open_set, (f_scores[neighbor.id], neighbor))

        # 若无法找到路径，抛出异常
        raise ValueError("No path found from start to goal.")