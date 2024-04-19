#include <iostream>
#include "data.hpp"

int main() {
    Graph graph;

    // 添加节点和边（假设图是有向的）
    graph.addNode(0);
    graph.addNode(1);
    graph.addNode(2);
    graph.addNode(3);
    graph.addEdge(0, 1, 10);
    graph.addEdge(0, 2, 15);
    graph.addEdge(1, 2, 7);
    graph.addEdge(1, 3, 0.25);
    graph.addEdge(2, 3, 0.75);

    // 定义启发式函数（例如曼哈顿距离）
    auto heuristic = [](int currentId, int goalId) {
        // 这里仅作演示，实际距离需要根据节点间实际位置计算
        return std::abs(currentId - goalId);
    };

    // 使用A*算法寻找从节点0到节点3的最短路径
    std::vector<int> shortestPath = graph.aStarSearch(0, 3, heuristic);

    // 输出路径
    std::cout << "Shortest path: ";
    for (int nodeId : shortestPath) {
        std::cout << nodeId << " ";
    }
    std::cout << std::endl;

    return 0;
}