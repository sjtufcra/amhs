import * as THREE from './three.m.js';
import { FontLoader } from './FontLoader.js';
import { OrbitControls } from './OrbitControls.js';
// import {fetchR} from "../server/xhr.js"

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.01, 10000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

scene.background = new THREE.Color(0xf0f0f0);

var count = 0;

var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

var raw = JSON.stringify({
  "start": 123,
  "end": 345
});

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};


const path = await fetch("http://0.0.0.0:8055/getpath/", requestOptions)
const ComPath = await path.json()

// 添加 OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);

// 示例数据
// const nodes = [
//   { id: 1, label: 'Node 1' ,position:{x:0,y:0}},
//   { id: 2, label: 'Node 2' ,position:{x:30,y:17}},
//   { id: 3, label: 'Node 3' ,position:{x:-60,y:32}},
// ];

// const edges = [
//   { source: nodes[0], target: nodes[1] },
//   { source: nodes[1], target: nodes[2] },
// ];

// 真实数据
const response = await fetch('http://0.0.0.0:8055/getNodes/');
const edges = await fetch('http://0.0.0.0:8055/getEdges/');

const nodes = JSON.parse(await response.json());
const edgs = JSON.parse(await edges.json())


// 测试数据
// const response = await fetch('http://127.0.0.1:5500/test/html/json/node.json')
// const node = await response.json()
// const edges = await fetch('http://127.0.0.1:5500/test/html/json/edge.json')
// const edg = await edges.json()





// 生成随机数
function createNumber(){
  function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }
  
  const minValue = 0; // 设置最小值
  const maxValue = 9999; // 设置最大值（确保范围内数字数量大于等于3832）
  
  // 生成包含所有可能数字的数组
  const allNumbers = Array.from({ length: maxValue - minValue + 1 }, (_, index) => index + minValue);
  
  // 使用 Fisher-Yates shuffle 打乱数组
  shuffleArray(allNumbers);
  
  // 截取前3832个数字
  const randomNumbers = allNumbers.slice(0, 3832);
  return randomNumbers;
  
}

const z_position = createNumber()

async function loadFontAndCreateNodes() {
  const fontLoader = new FontLoader();
  const fontResponse = await fetch('https://threejs.org/examples/fonts/helvetiker_regular.typeface.json');
  const fontData = await fontResponse.json();
  const font = fontLoader.parse(fontData);
  
  nodes.forEach(node => {

    const nodeObject = createNode(node, font,count,z_position);
    // nodeObject.position.set(Math.random() * 4 - 2, Math.random() * 4 - 2, 0);
    if(nodeObject)scene.add(nodeObject);
    count++
  });

  edgs.forEach(edge => {
    for(var x=0;x<nodes.length;x++){
      if(edge.start[0] == nodes[x].position[0] && edge.start[1] == nodes[x].position[1]){
        edge.start.z = nodes[x].z_position
      }
      if(edge.end[0] == nodes[x].position[0] && edge.end[1] == nodes[x].position[1]){
        edge.end.z = nodes[x].z_position
      }
    }
    const edgeObject = createEdge(edge.start, edge.end,edge.weight);
    if (edgeObject){scene.add(edgeObject);}
  });

  camera.position.z = 50;

  animate();
}

async function loadAndRender() {
  await loadFontAndCreateNodes();
}

function createNode(node, font,count,z_position) {
  let color = 0x333333
  let boo = 0.4
  let visible = false
  let radius = 0.6
  for(var x = 0; x < ComPath.length; x++){
    if (ComPath[x][0] == node.position[0] && ComPath[x][1] == node.position[1]){
      if(x==0){
        color = 0x35b2f9
      }else{
        if(x==ComPath.length-1){
          color = 0xff0000
        }else{
          color = 0x31f352
          boo = 0.6
          radius = 0.2
        }
      }
      boo = 1
      radius = 1
      visible = true
      break;
    }
  }
  // 单独显示路径
  if(visible){
  // if(true){
  const sphere = createNodeGeometry(radius,color,boo);
  const text = createTextNode(node.id, font);
  text.position.z = 0.1;
  text.position.x = -0.24;

  const group = new THREE.Group();
  group.add(sphere);
  group.add(text);
  group.position.x = node.position[0];
  group.position.y = node.position[1];
  group.position.z = z_position[count]*0.01;
  node.z_position = group.position.z;
  return group;
  }
  
}

function createTextNode(label, font) {
    const shapes = font.generateShapes( label,10 );
    const geometry = new THREE.ShapeGeometry( shapes );
    geometry.scale(0.05, 0.05, 0.05)
    // geometry.computeBoundingBox();

    // const xMid = - 0.5 * ( geometry.boundingBox.max.x - geometry.boundingBox.min.x );

    // geometry.translate( xMid, 0, 0 );

    // make shape ( N.B. edge view not visible )

    // const text = new THREE.Mesh( geometry, matLite );
    // text.position.z = - 150;
    // scene.add( text );
//   const textGeometry = new TextGeometry(label, {
//     font,
//     size: 0.1,
//     height: 0.1,
//     depth: 0.1,
//   });
//   const textMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
    const matLite = new THREE.MeshBasicMaterial( {
        color: 0x006699,
        transparent: true,
        opacity: 0.8,
        side: THREE.DoubleSide
    } );
  return new THREE.Mesh(geometry, matLite);
//   return new THREE.Mesh(geometry, textMaterial);
}

function createNodeGeometry(radius, color,opacity) {
  const geometry = new THREE.SphereGeometry(radius, 16, 16);
  const material = new THREE.MeshBasicMaterial({ color ,opacity: opacity, transparent: true});
  return new THREE.Mesh(geometry, material);
}

function createEdge(source, target,weight) {
  // const start = new THREE.Vector3(source[0], source[1], 0);  // 箭头起点位置
  // const direction = new THREE.Vector3(target[0], target[1], 0);  // 箭头指向的方向（这里指向 x 轴正方向）
  // const length = 10;  // 箭头总长度
  // const headLength = 2;  // 箭头头部长度
  // const headWidth = 1;  // 箭头头部宽度
  // const color = 0xff00ff;  // 箭头颜色（红色）
  // const arrow = new THREE.ArrowHelper(direction, start, length, color, headLength, headWidth);
  // return arrow
  let colors = 0xff00ff;
  let wd = 1;
  let opacity = 0.3;
  let bool = false
  let ss = 0;
  let ee = 0;
  for(var x = 0; x < ComPath.length; x++){
    if (ComPath[x][0] == source[0] && ComPath[x][1] == source[1]){
      colors = 0x35b2f9
      wd = 10
      opacity = 1
      bool = true
      ss = 1
    }
  }
  const lineGeometry = new THREE.BufferGeometry().setFromPoints([{x:source[0],y:source[1],z:source.z}, {x:target[0],y:target[1],z:target.z}]);
  if (bool){
    for(var x = 0; x < ComPath.length; x++){
      if (ComPath[x][0] == target[0] && ComPath[x][1] == target[1]){
        ee = 1
        break
      }
    }
  if(ee==1){
    if(weight>5 && weight<=7){
      colors = 0xff00ff
    }else{
      if (weight>7 && weight<=10){
        colors = 0xffff00
      }else{
        if (weight>0 && weight<=2){
          colors = 0x2eaa16
        }else{
          colors = 0x212121
        }
      }
  }
  const lineMaterial = new THREE.LineBasicMaterial({ color: colors,opacity:opacity });
  return new THREE.Line(lineGeometry, lineMaterial);
  }
  }
  
}

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
  controls.update(); // 更新 OrbitControls
}

loadAndRender();