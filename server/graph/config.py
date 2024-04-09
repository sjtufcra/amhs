# 各项参数配置表

# 数据文件列表
jsonPath = "./data/adjacent_matrix_test1.json"

# 服务器参数
httpServer = dict(uname ='0.0.0.0',
    paths = "src.api:app",
    ports = 8055,
    log = 'info',
    reloade =True)