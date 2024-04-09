# 示例代码
from srccode import a_star_search, Node

# 数据格式
grid = [
    ['S', ' ', ' ', ' ', ' '],
    [' ', ' ', '#', ' ', ' '],
    [' ', '#', ' ', ' ', ' '],
    ['#', ' ', ' ', 'G', ' ']
]

start_node = Node(0, 0)
goal_node = Node(3, 3)

# 生成网格
grids = [[Node(x, y) for y in range(len(grid[0]))] for x in range(len(grid))]

# 提取障碍物
obstacles = {(x, y) for x, row in enumerate(grid) for y, cell in enumerate(row) if cell == '#'}

# 计算最优路径
path = a_star_search(
    start_node,
    goal_node,
    grids,
    obstacles
)

# 输出结果
if path:
    print(f"Found path: {path}")
else:
    print("No path found.")