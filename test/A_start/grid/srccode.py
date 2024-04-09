import heapq

class Node:
    def __init__(self, x, y):
            """
        类的初始化方法。
        
        参数:
        - x: 初始化对象的x坐标。
        - y: 初始化对象的y坐标。
        
        属性:
        - x: 对象的x坐标。
        - y: 对象的y坐标。
        - g: 从起始点到当前点的实际距离成本。
        - h: 从当前点到目标点的估算距离成本。
        - f: g和h的总和，用于A*搜索算法中节点的排序。
        - parent: 当前节点的父节点，用于回溯路径。
        """
            self.x = x
            self.y = y
            self.g = float('inf')  # 初始化g值为无穷大，表示起始点到当前点的距离成本
            self.h = float('inf')  # 初始化h值为无穷大，表示当前点到目标点的估算距离成本
            self.f = float('inf')  # 初始化f值为无穷大，f = g + h
            self.parent = None  # 初始化父节点为None，用于记录路径
    def __lt__(self, other):
        return self.f < other.f


def heuristic(a, b):
    """
    使用曼哈顿距离作为启发式函数
    
    参数:
    a - 表示一个点的对象，该对象必须有 x 和 y 属性
    b - 同样表示一个点的对象，也有 x 和 y 属性
    
    返回值:
    两个点之间的曼哈顿距离（即横向和纵向距离之和的绝对值）
    """
    return abs(a.x - b.x) + abs(a.y - b.y)

def a_star_search(start, goal, grid, obstacles=None):
    """
    实现A*搜索算法以寻找从起点到目标点的最短路径。
    
    参数:
    - start: 起点对象,须有x, y属性标识位置。
    - goal: 目标对象,须有x, y属性标识位置。
    - grid: 二维列表表示的网格环境。
    - obstacles: 障碍物集合，可选，默认为空。包含不可通过的网格位置。
    
    返回值:
    - 如果找到路径,返回一个包含路径点坐标的列表;否则返回None。
    """
    # 处理默认障碍物为空的情况
    if obstacles is None:
        obstacles = set()

    # 初始化开放列表和关闭列表
    open_list = []
    heapq.heappush(open_list, (start.h, start))

    closed_list = {}  # 使用字典存储节点及其对应的g值，便于快速查找和更新

    # 初始化起点属性
    start.g = 0
    start.h = heuristic(start, goal)
    start.f = start.g + start.h
    grid[start.x][start.y]=start
    grid[goal.x][goal.y]=goal

    # 循环搜索直到找到目标或开放列表为空
    while open_list:
        _, current = heapq.heappop(open_list)

        # 找到目标，构建并返回路径
        if current == goal:
            path = []
            while current is not None:
                path.append((current.x, current.y))
                current = current.parent
            path.reverse()
            return path

        closed_list[current] = current.g  # 将节点及其g值添加到closed_list

        # 遍历当前节点的四个邻居
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor_x = current.x + dx
            neighbor_y = current.y + dy

            # 跳过不可访问的邻居节点包括父节点：障碍物、父节点
            if neighbor_x < 0 or neighbor_y < 0 or \
                    neighbor_x >= len(grid) or neighbor_y >= len(grid[0]) or \
                    (neighbor_x, neighbor_y) in obstacles:
                continue
            if current.parent and (neighbor_x, neighbor_y) == (current.parent.x,current.parent.y):
                    continue

            neighbor = grid[neighbor_x][neighbor_y]

            # 计算潜在的从当前节点到邻居节点的代价
            tentative_g = current.g + 1  # 假设移动成本为1

            # 跳过已评估或更好路径的邻居节点
            if neighbor in closed_list and tentative_g >= neighbor.g:  # 更改此处的判断逻辑
                continue

            # 更新邻居节点的属性
            neighbor.g = tentative_g
            neighbor.h = heuristic(neighbor, goal)
            neighbor.f = neighbor.g + neighbor.h
            neighbor.parent = current

            # 将新发现的节点加入到开放列表
            if neighbor not in open_list:
                heapq.heappush(open_list, (neighbor.f, neighbor))

    # 如果没有找到路径，返回None
    return None