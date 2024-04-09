import * as PIXI from './pixi.js';
import * as config from '../../config/px.js'

// 获取 canvas 元素
const canvas = document.getElementById('topology-canvas');

// 创建 Pixi 应用
const app = new PIXI.Application();
await app.init({
    view: canvas,
    width: window.innerWidth,
    height: window.innerHeight,
    backgroundColor: 0xf0f0f0,
  })

// 添加到 DOM 中
document.body.appendChild(app.canvas);

// 创建节点
function createNode(x, y, radius, color) {
    const nodeGraphics = new PIXI.Graphics();
  
    nodeGraphics.beginFill(color);
    nodeGraphics.drawCircle(x, y, radius);
    nodeGraphics.endFill();
  
    return nodeGraphics;
  }
  
// 创建边
  function createEdge(fromNode, toNode, color) {
    const edgeGraphics = new PIXI.Graphics();
  
    edgeGraphics.lineStyle(2, color, 1);
    edgeGraphics.moveTo(fromNode.x, fromNode.y);
    edgeGraphics.lineTo(toNode.x, toNode.y);
  
    return edgeGraphics;
  }

// 真实数据
const response = await fetch('http://0.0.0.0:8055/getNodes/');
const edge = await fetch('http://0.0.0.0:8055/getEdges/');

var raw = JSON.stringify({
  "start": 123,
  "end": 345
});

var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};
const path = await fetch("http://0.0.0.0:8055/getpath/", requestOptions)
const ComPath = await path.json()

const nodesData = JSON.parse(await response.json());
const edgesData = JSON.parse(await edge.json())
  

  nodesData.forEach((nodeData) => {
    const node = createNode(nodeData.position[0], nodeData.position[1],2,0x0000FF);
    app.stage.addChild(node);
  });

//   edgesData.forEach((edgeData) => {
//     const fromNode = nodes.find((n) => n.id === edgeData.fromId);
//     const toNode = nodes.find((n) => n.id === edgeData.toId);
//     const edge = createEdge(fromNode, toNode, edgeData.color);
//     app.stage.addChild(edge);
//   });




// 测试数据
// const topologyData = {
//     nodes: [
//       { id: 1, x: 100, y: 100, radius: 20, color: 0xFF0000 },
//       { id: 2, x: 300, y: 300, radius: 20, color: 0x00FF00 },
//       { id: 3, x: 500, y: 200, radius: 20, color: 0x0000FF },
//       { id: 4, x: 600, y: 900, radius: 20, color: 0x0000FF },
//       { id: 5, x:670, y: 220, radius: 20, color: 0x0000FF },
//       { id: 1, x: 10, y: 50, radius: 20, color: 0xFF0000 },
//       { id: 2, x: 210, y: 280, radius: 20, color: 0x00FF00 },
//       { id: 3, x: 890, y: 450, radius: 20, color: 0x0000FF },
//       { id: 4, x: 120, y: 760, radius: 20, color: 0x0000FF },
//       { id: 5, x: 230, y: 430, radius: 20, color: 0x0000FF },
//     ],
//     edges: [
//       { from: 1, to: 2 },
//       { from: 2, to: 3 },
//       { from: 3, to: 1 },
//     ],
//   };
  
  // 创建节点和边
  // const nodes = topologyData.nodes.map(nodesData => createNode(nodeData.x, nodeData.y, nodeData.radius, nodeData.color));
  // const edges = topologyData.edges.map(edgesData => createEdge(nodes[edge.from - 1], nodes[edge.to - 1], 0x000000));
  
  // 添加节点和边到舞台
  // nodes.forEach(node => app.stage.addChild(node));
  // edges.forEach(edge => app.stage.addChild(edge));