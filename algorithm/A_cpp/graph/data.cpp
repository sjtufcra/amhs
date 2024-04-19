#include "data.hpp"
#include <iostream>

void Graph::addNode(int id) {
    nodes[id] = GraphNode{id, 0.0};
}

void Graph::addEdge(int srcId, int dstId, double cost) {
    nodes[srcId].neighbors.push_back({dstId, cost});
    // 若图是无向的，还需添加反向边：
    // nodes[dstId].neighbors.push_back({srcId, cost});
}

std::vector<int> Graph::aStarSearch(int startId, int goalId,
                                   std::function<double(int, int)> heuristic) {
    std::unordered_map<int, double> g_cost;  // 从起点到各节点的实际代价
    std::unordered_map<int, double> f_cost;  // 评估函数f(n) = g(n) + h(n)
    std::unordered_map<int, int> came_from;  // 记录节点的前驱节点

    std::priority_queue<std::pair<double, int>, std::vector<std::pair<double, int>>, std::greater<std::pair<double, int>>> openSet;
    openSet.push({0, startId});

    g_cost[startId] = 0;
    f_cost[startId] = heuristic(startId, goalId);

    while (!openSet.empty()) {
        int currentId = openSet.top().second;
        openSet.pop();

        if (currentId == goalId) {
            // 找到目标节点，回溯构建路径
            std::vector<int> path;
            while (currentId != startId) {
                path.push_back(currentId);
                currentId = came_from[currentId];
            }
            path.push_back(startId);
            std::reverse(path.begin(), path.end());
            return path;
        }

        for (const auto &edge : nodes[currentId].neighbors) {
            int neighborId = edge.dstId;
            double tentative_g_cost = g_cost[currentId] + edge.cost;

            if (tentative_g_cost < g_cost[neighborId]) {
                came_from[neighborId] = currentId;
                g_cost[neighborId] = tentative_g_cost;
                f_cost[neighborId] = g_cost[neighborId] + heuristic(neighborId, goalId);
                openSet.push({f_cost[neighborId], neighborId});
            }
        }
    }

    return {};  // 若未找到路径，返回空向量
}