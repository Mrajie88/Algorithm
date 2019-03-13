import numpy as np
import pandas as pd
import random
import plotly.plotly as py
from plotly import tools
from plotly.graph_objs import *
tools.set_credentials_file(username='Worldzhang', api_key='OU3H87MJxDBEGP45zQa3')
def cluster(data,k):
    #计算初始
    cluster_center = {}
    cluster_record = {}
    ran_num =[random.randint(0, len(data)-1) for _ in range(k)]
    print(ran_num)
    count = 1
    for each in ran_num:
        cluster_center[count] = data.values[each]
        count = count+1
    for each in data.index:
        minDist = 10000
        for center in cluster_center:
            dist = np.linalg.norm(data.loc[each].values[0:] - cluster_center[center].tolist()[:])
            if(dist<minDist):
                minDist = dist
                cluster_record[each] = center
    #print(cluster_record)


    cluster_center_temp = {}
    for each in cluster_center.keys():
        i = 0
        s = []
        for i in cluster_record:
            if (cluster_record[i] == each):
                s.append(data.loc[i].values[0:])
        a = np.mean(np.array(s), axis=0)
        cluster_center_temp[each] = a
    # 计算各个簇得平均值并且让其成为新的中心点 直到位置变化很小
    tag = 0
    while tag!=1:
    #重新赋值cluster_center
        for each in cluster_center:
            cluster_center[each] = cluster_center_temp[each]
        #重新计算各个数据到簇中心距离
        for each in data.index:
            minDist = 10000
            for center in cluster_center:
                dist = np.linalg.norm(data.loc[each].values[0:] - cluster_center[center].tolist()[:])
                if(dist<minDist):
                    minDist = dist
                    cluster_record[each] = center
        #print(cluster_record)
        for each in cluster_center.keys():
            i = 0
            s = []
            for i in cluster_record:
                if (cluster_record[i] == each):
                    s.append(data.loc[i].values[0:])
            #print(s)
            a = np.mean(np.array(s), axis=0)
            cluster_center_temp[each] = a
        tag1 = 0
        tag2 = 0
        #验证簇中心是否移动
        for each in cluster_center:
            tag1+=np.mean(cluster_center[each])
            tag2+=np.mean(cluster_center_temp[each])
        if(abs(tag1-tag2)<0.0001):
            tag = 1
        else:
            tag = 0
    return cluster_record, cluster_center
    #进行可视化处理

"""
使用iris数据集 进行K-means算法
"""
#读取数据集
data = pd.read_csv("data/iris.csv")
data_key = []
data_class = []
data_color = []
del data[' class']
data = data.apply(lambda x:(x-np.min(x))/(np.max(x)-np.min(x)))
cluster_record,cluster_center = cluster(data,3)
for each in cluster_record:
    data_key.append(each)
    data_class.append(cluster_record[each])
    if(cluster_record[each]==1):
        data_color.append('red')
    if (cluster_record[each] == 2):
        data_color.append('blue')
    if (cluster_record[each] == 3):
        data_color.append('green')
#可视化处理
trace0 = Scatter(
        x=data_key,
        y=data_class,
        marker=dict(
            color=data_color,
        ),
        mode='markers'
    )

data = Data([trace0])

py.iplot(data)

