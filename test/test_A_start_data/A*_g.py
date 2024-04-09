from graph import  *
# 示例：构建一个简单的图结构
graph = Graph()

# 添加节点
node_a = Node(id=0, coordinates=(0, 0))
node_b = Node(id=1, coordinates=(1, 0))
node_c = Node(id=2, coordinates=(2, 0))
graph.add_node(node_a)
graph.add_node(node_b)
graph.add_node(node_c)

# 添加边
edge_ab = Edge(start=node_a, end=node_b, weight=1.0)
edge_bc = Edge(start=node_b, end=node_c, weight=1.0)
graph.add_edge(edge_ab)
graph.add_edge(edge_bc)

# 设置起点和终点
graph.set_start_and_goal(start_node=node_a, goal_node=node_c)