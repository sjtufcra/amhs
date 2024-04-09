
from fastapi import FastAPI
# 自定义模块
from server.graph.src.data import *
from fastapi.middleware.cors import CORSMiddleware

# 参数表
app = FastAPI()
Gdata = Data()
   
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 直接获取路径
@app.post('/getpath/')
def getPath(data:dict):
    start = Gdata.nodes[data.get('start')]
    end = Gdata.nodes[data.get('end')]
    graph = Gdata.Graph
    graph.set_start_and_goal(start,end)
    try:
        astart = AStar()
        shortest_path_nodes = astart.a_star_search(graph)
        corrd = [node.coordinates for node in shortest_path_nodes]
        return corrd
    except ValueError as e:
        print(e)

@app.get('/getNodes/')
def getNodes():
    if Gdata.nodes is None:
        return []
    node = json.dumps(Gdata.nodes,cls=NodeEncoder)
    return node

@app.get('/getEdges/')
def getEdges():
    if Gdata.edges is None:
        return []
    edge = json.dumps(Gdata.edges,cls=EdgeEncoder)
    return edge
