# 跨目录访问
import sys
from os import path
# 这里相当于把相对路径 .. 添加到pythonpath中
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


# 自定义模块

from config import *
from httpServer import *

if __name__ == "__main__":
    sh = Server(**httpServer)
    sh.run()