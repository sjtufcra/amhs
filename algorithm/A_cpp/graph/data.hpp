#ifndef data_hpp
#define data_hpp
#include <vector>
#include <queue>
#include <unordered_map>

// 定义Edge和GraphNode结构
struct Edge {
    int dstId;
    double cost;
};

struct GraphNode {
    int id;
    double cost;
    std::vector<Edge> neighbors;
};

// 定义Graph类
class Graph {
public:
    void addNode(int id);
    void addEdge(int srcId, int dstId, double cost);
    std::vector<int> aStarSearch(int startId, int goalId,
                                 std::function<double(int, int)> heuristic);

private:
    std::unordered_map<int, GraphNode> nodes;
};

#endif 