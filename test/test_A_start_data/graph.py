from typing import Dict, List, Tuple

class Node:
    """
    图节点类，包含节点编号和坐标信息。
    """
    def __init__(self, id: int, coordinates: Tuple[float, float]):
        self.id = id
        self.coordinates = coordinates

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
        self.adjacency_matrix[(edge.end.id, edge.start.id)] = edge.weight  # 对于无向图，双向添加权重

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

