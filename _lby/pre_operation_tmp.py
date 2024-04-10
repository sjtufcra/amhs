import pandas as pd
import warnings
import networkx as nx


def adjacent_matrix():
    d0 = pd.read_excel('./台位坐标.xlsx')
    d = pd.read_excel('./轨道坐标.xlsx')
    # 添加轨道的编号
    name_l = []
    for i in d['起始节点'].unique():
        name_l.append(str(i))
    # 添加台位的编号
    name_w = []
    for i in d0['唯一ID'].unique():
        name_w.append(str(i))
    name_l.extend(name_w)
    worker_loc = pd.DataFrame(columns=['id', '起点', '终点', '起终点', '距起点长度', '距终点长度'])
    for i in d0.index:
        id = str(d0['唯一ID'][i])
        sl = d0['所在轨道起点'][i]
        el = d0['所在轨道终点'][i]
        dis0 = d0['X坐标'][i]
        dis1 = d.loc[(d['起始节点'] == sl) & (d['终止节点'] == el)]['起始坐标'].values[0]
        dis2 = d.loc[(d['起始节点'] == sl) & (d['终止节点'] == el)]['终点坐标'].values[0]
        worker_loc.loc[len(worker_loc)] = [id, sl, el, str(sl) + ',' + str(el), dis0 - dis1, dis2 - dis0]
    # 邻接矩阵
    m1 = pd.DataFrame(0, columns=name_l, index=name_l)
    # 加权邻接矩阵
    m2 = pd.DataFrame(0, columns=name_l, index=name_l)
    for i in d.index:
        m1[str(d['终止节点'][i])][str(d['起始节点'][i])] = 1
        m2[str(d['终止节点'][i])][str(d['起始节点'][i])] = d['终点坐标'][i] - d['起始坐标'][i]
    for i in worker_loc['起终点'].unique():
        w0 = worker_loc.loc[worker_loc['起终点'] == i]
        w1 = w0.sort_values('距起点长度', ascending=True)
        w1 = w1.reset_index(drop=True)
        if len(w1) > 1:
            for j in w1.index:
                if w1['距起点长度'][j] == min(w1['距起点长度']):
                    m1[str(w1['起点'][j])][str(w1['id'][j])] = 1
                    m2[str(w1['起点'][j])][str(w1['id'][j])] = w1['距起点长度'][j]
                    m1[str(w1['id'][j])][str(w1['id'][j+1])] = 1
                    m2[str(w1['id'][j])][str(w1['id'][j+1])] = w1['距起点长度'][j+1] - w1['距起点长度'][j]
                elif w1['距起点长度'][j] == max(w1['距起点长度']):
                    m1[str(w1['id'][j])][str(w1['终点'][j])] = 1
                    m2[str(w1['id'][j])][str(w1['终点'][j])] = w1['距终点长度'][j]
                else:
                    m1[str(w1['id'][j])][str(w1['id'][j + 1])] = 1
                    m2[str(w1['id'][j])][str(w1['id'][j + 1])] = w1['距起点长度'][j + 1] - w1['距起点长度'][j]
        elif len(w1) == 1:
            m1[str(w1['起点'][0])][str(w1['id'][0])] = 1
            m2[str(w1['起点'][0])][str(w1['id'][0])] = w1['距起点长度']
            m1[str(w1['id'][0])][str(w1['终点'][0])] = 1
            m2[str(w1['id'][0])][str(w1['终点'][0])] = w1['距终点长度']
    for i in m1.index:
        m1[i][i] = 1
    m1.to_excel('./天车轨道台位邻接矩阵.xlsx')
    m2.to_excel('./天车轨道台位加权邻接矩阵.xlsx')
    return m1, m2


def shortest_path():
    # d0 = pd.read_excel('./天车轨道台位邻接矩阵.xlsx')
    d1 = pd.read_excel('./天车轨道台位加权邻接矩阵.xlsx', index_col=0)
    g = nx.DiGraph()
    for i in d1.columns:
        for j in d1.index:
            if d1[i][j] > 0:
                g.add_weighted_edges_from([(str(j), str(i), d1[i][j])])
    sp = nx.all_pairs_bellman_ford_path(g)
    all_path = pd.DataFrame(columns=['起点', '终点', '路径'])
    for i in sp:
        for j, k in i[1].items():
            all_path.loc[len(all_path)] = [i[0], j, k]
    all_path.to_excel('./天车全路径.xlsx')
    return 0


warnings.filterwarnings('ignore')
# 原始数据转为邻接矩阵
adjacent_matrix()
# 计算所有节点的最短路径
shortest_path()
