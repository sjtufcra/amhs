var dom = document.getElementById('container');
var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});
var app = {};

var option;

const names = [
    'Path1',
    'Path2',
    'Path3',
    'Path4',
    'Path5',
    'Path6',
    'Path7',
    'Path8',
    'Path9'
];

const nodes = ['node1', 'node2', 'node3', 'node4', 'node5', 'node6'];
const shuffle = (array) => {
    let currentIndex = array.length;
    let randomIndex = 0;
    while (currentIndex > 0) {
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex--;
        [array[currentIndex], array[randomIndex]] = [
            array[randomIndex],
            array[currentIndex]
        ];
    }
    return array;
};
const generateRankingData = () => {
    const map = new Map();
    const defaultRanking = Array.from({ length: names.length }, (_, i) => i + 1);
    for (const _ of nodes) {
        const shuffleArray = shuffle(defaultRanking);
        names.forEach((name, i) => {
            map.set(name, (map.get(name) || []).concat(shuffleArray[i]));
        });
    }
    return map;
};
const generateSeriesList = () => {
    const seriesList = [];
    const rankingMap = generateRankingData();
    rankingMap.forEach((data, name) => {
        const series = {
            name,
            symbolSize: 20,
            type: 'line',
            smooth: true,
            emphasis: {
                focus: 'series'
            },
            endLabel: {
                show: true,
                formatter: '{a}',
                distance: 20
            },
            lineStyle: {
                width: 4
            },
            data
        };
        seriesList.push(series);
    });
    return seriesList;
};
option = {
    title: {
        text: '路径拓扑图'
    },
    tooltip: {
        trigger: 'item'
    },
    grid: {
        left: 30,
        right: 110,
        bottom: 30,
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        splitLine: {
            show: true
        },
        axisLabel: {
            margin: 30,
            fontSize: 16
        },
        boundaryGap: false,
        data: nodes
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            margin: 30,
            fontSize: 16,
            formatter: 'Start{value}'
        },
        inverse: true,
        interval: 1,
        min: 1,
        max: names.length
    },
    series: generateSeriesList()
};


if (option && typeof option === 'object') {
    myChart.setOption(option);
}

window.addEventListener('resize', myChart.resize);