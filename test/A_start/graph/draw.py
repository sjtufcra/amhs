import networkx as nx
import matplotlib.pyplot as plt


# 绘制一个有向图的表达式
def draw_graph(G):
    if hasattr(G, '_node'):
        if any('coordinates' in data for node, data in G.nodes(data=True)):
            pos = {node: data['coordinates'] for node, data in G.nodes(data=True) if 'coordinates' in data}
            has_pos = True
        else:
            has_pos = False
    else:
        has_pos = False

    if not has_pos:
        print("警告：图 G 中未找到节点位置信息，将使用随机布局。")
        pos = nx.random_layout(G)
    else:
        print("正在使用图 G 中的节点位置信息进行绘制。")

    # 绘制节点和边
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G, pos, edge_color='gray')

    # 添加节点标签
    nx.draw_networkx_labels(G, pos, font_size=10)

    # 显示图形
    plt.axis('off')
    plt.show()

