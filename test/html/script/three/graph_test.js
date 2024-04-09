import * as THREE from './three.m.js';
import * as FontLoader from './FontLoader.js';
import * as TextGeometry from './TextGeometry.js';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 示例数据
const nodes = [
  { id: 1, label: 'Node 1' },
  { id: 2, label: 'Node 2' },
  { id: 3, label: 'Node 3' },
];

const edges = [
  { source: nodes[0], target: nodes[1] },
  { source: nodes[1], target: nodes[2] },
];
const bb = new FontLoader.FontLoader()
const refo = await fetch('https://threejs.org/examples/fonts/helvetiker_regular.typeface.json')
const data = await refo.json()
const fonts = bb.parse(data)

function createNodeGeometry(radius, color) {
  const geometry = new THREE.SphereGeometry(radius, 16, 16);
  const material = new THREE.MeshBasicMaterial({ color });
  return new THREE.Mesh(geometry, material);
}

function createTextNode(label) {
  const textGeometry = new TextGeometry.TextGeometry(label, {
    font: fonts,
    size: 0.5,
    height: 0.1,
    curveSegments: 12,
  });
  const textMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
  return new THREE.Mesh(textGeometry, textMaterial);
}

function createNode(node) {
  const sphere = createNodeGeometry(0.3, 0xff0000);
  const text = createTextNode(node.label);
  text.position.z = -0.24;

  const group = new THREE.Group();
  group.add(sphere);
  group.add(text);

  return group;
}

function createEdge(source, target) {
  const lineGeometry = new THREE.BufferGeometry().setFromPoints([source.position, target.position]);
  const lineMaterial = new THREE.LineBasicMaterial({ color: 0x0000ff });
  return new THREE.Line(lineGeometry, lineMaterial);
}

nodes.forEach(node => {
  const nodeObject = createNode(node);
  nodeObject.position.set(Math.random() * 4 - 2, Math.random() * 4 - 2, 0);
  scene.add(nodeObject);
});

// edges.forEach(edge => {
//   const edgeObject = createEdge(edge.source, edge.target);
//   scene.add(edgeObject);
// });

camera.position.z = 0.33;

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}

animate();