import * as PIXI from "pixi.js";

debugger
const app = new PIXI.Application({
    width: window.innerWidth,
    height: window.innerHeight,
    backgroundColor: 0x222222,
});
document.body.appendChild(app.view);

// 图结构数据
const nodes = [{id: "A"}, {id: "B"}, {id: "C"}];
const links = [{source: "A", target: "B"}, {source: "A", target: "C"}];

const nodeRadius = 10;
const linkWidth = 2;
const linkColor = 0xFFFFFF;

// 创建节点精灵
const nodeSprites = nodes.map(node => {
    const sprite = new PIXI.Sprite(PIXI.Texture.WHITE);
    sprite.tint = 0xFF0000; // 设置节点颜色
    sprite.width = nodeRadius * 2;
    sprite.height = nodeRadius * 2;
    sprite.anchor.set(0.5); // 将锚点设置为中心
    app.stage.addChild(sprite); // 将节点添加到舞台
    return {node, sprite};
});

// 创建边精灵（线段）
const linkGraphics = new PIXI.Graphics();
app.stage.addChild(linkGraphics);

// 绘制边
links.forEach(link => {
    const sourceNode = nodeSprites.find(n => n.node.id === link.source);
    const targetNode = nodeSprites.find(n => n.node.id === link.target);
    if (sourceNode && targetNode) {
        const dx = targetNode.sprite.x - sourceNode.sprite.x;
        const dy = targetNode.sprite.y - sourceNode.sprite.y;
        const length = Math.sqrt(dx ** 2 + dy ** 2);

        linkGraphics.lineStyle(linkWidth, linkColor, 1);
        linkGraphics.moveTo(sourceNode.sprite.x, sourceNode.sprite.y);
        linkGraphics.lineTo(
            sourceNode.sprite.x + dx / length * nodeRadius,
            sourceNode.sprite.y + dy / length * nodeRadius
        );
        linkGraphics.lineTo(
            targetNode.sprite.x - dx / length * nodeRadius,
            targetNode.sprite.y - dy / length * nodeRadius
        );
        linkGraphics.lineTo(targetNode.sprite.x, targetNode.sprite.y);
        linkGraphics.closePath();
    }
});

// 示例动画：节点随机移动
app.ticker.add(() => {
    nodeSprites.forEach(n => {
        n.sprite.x = Math.random() * app.screen.width;
        n.sprite.y = Math.random() * app.screen.height;
    });
});