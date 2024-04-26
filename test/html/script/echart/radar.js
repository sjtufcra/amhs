var dom = document.getElementById('container');
var myChart = echarts.init(dom, null, {
  renderer: 'canvas',
  useDirtyRect: false
});
var app = {};
var option;
option = {
  title: {
    text: '性能优化分析'
  },
  legend: {
    data: ['Old algorithm', 'New algorithm']
  },
  radar: {
    // shape: 'circle',
    indicator: [
      { name: 'task/ms', max: 5000 },     // task/ms 单个任务处理时长，单位时长ms
      { name: 'batch/ms', max: 30000 },   // batch/ms 批处理时长，单位时长ms
      { name: 'minute/t', max: 4000 },    // minute/t 每分钟处理任务数
      { name: 'hour/t', max: 38000 },     // hour/t 每小时处理任务数
      { name: 'average/h', max: 25000 },  // average/h 每小时平均处理任务数
      { name: 'peak/b', max: 999 }        // peak/b 峰值 每一批次处理任务数
      
    ]
  },
  series: [
    {
      name: 'Old vs New',
      type: 'radar',
      data: [
        {
          value: [2500, 10000, 55, 420, 437.2, 430],
          name: 'Old algorithm',
          label: {
            show: true,
            position: 'left',
            fontSize: 8,
            color: 'rgba(83, 112, 198, 1)',
            formatter: function (params) {
              return params.value;
            }
          }
        },
        {
          value: [247, 3200, 240, 15400, 16200, 370],
          name: 'New algorithm',
          label: {
            show: true,
            position: 'right',
            fontSize: 10,
            color: 'rgba(0, 0, 0, 1)',
            formatter: function (params) {
              return params.value;
            }
          },
          areaStyle: {
            color: new echarts.graphic.RadialGradient(0.1, 0.6, 1, [
              {
                color: 'rgba(146, 203, 116, 0.1)',
                offset: 0
              },
              {
                color: 'rgba(146, 203, 116, 0.9)',
                offset: 1
              }
      ])
          }
        }
        

      ]
    }
  ]
};

if (option && typeof option === 'object') {
  myChart.setOption(option);
}

window.addEventListener('resize', myChart.resize);