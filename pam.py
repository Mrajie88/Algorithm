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
    cluster_record_temp = {}
    record_tag = {}
    cluster_cost = 0
    cluster_center_temp = {}
    cluster_center_temp2 = {}
    ran_num =[random.randint(0, len(data)-1) for _ in range(k)]
    print(ran_num)
    for each in data.index:
        record_tag[each] = 0
        count = 1
    for each in ran_num:
        cluster_center[count] = data.values[each]
        cluster_center_temp[count] = 100000
        cluster_center_temp2[count] = data.values[each]
        record_tag[each] = 1
        count = count+1
    #形成初始簇
    for each in data.index:
        minDist = 10000
        for center in cluster_center:
            dist = np.linalg.norm(data.loc[each].values[0:] - cluster_center[center].tolist()[:])
            if(dist<minDist):
                minDist = dist
                cluster_record[each] = center
                cluster_record_temp[each] = center
    #计算代价函数
    temp = 0
    for each in cluster_center:
        s = []
        for i in cluster_record:
            if (cluster_record[i] == each):
                s.append(data.loc[i].values[0:])
        for i in data.values[0:]:
            temp += np.linalg.norm(cluster_center[each] - i)
        if(temp<cluster_center_temp[each]):
            cluster_center_temp[each] = temp
        temp = 0
    for each in cluster_center:
        cluster_cost+=cluster_center_temp[each]
    #print("初始簇。。。。")
    #print(cluster_cost)
    #print(cluster_record)
    #print(cluster_center)

    # 计算各个簇并且让其成为新的中心点 直到位置变化很小
    #print("进入循环")
    #print(record_tag)
    tag = 0
    while tag!= 1:
        tag = 1
        for each in record_tag:
            if(each not in ran_num):
                record_tag[each] = 0
        #遍历每个簇
        temp_sum = 0
        for each in cluster_center.keys():
            s = {}
            #遍历每个未被选择过的点 并且计算到所有点距离
            for i in cluster_record:
                if (cluster_record[i] == each and record_tag[i]!=1):
                    s[i] = data.loc[i].values[0:]
            for i in s:
                #print(i)
                temp  = 0
                if ((s[i] != cluster_center[each]).all()):
                    for j in data.values[0:]:
                        temp += np.linalg.norm(s[i] - j)
                #print(temp,1)
                #print(cluster_center_temp[each])
                if(temp <= cluster_center_temp[each] and temp!=0):
                    cluster_center_temp[each] = temp
                    cluster_center_temp2[each] = s[i]
                record_tag[i] = 1

            temp_sum+=cluster_center_temp[each]
        #print("1111")
        #print(cluster_center_temp2)
        #print(cluster_center)
        if(temp_sum < cluster_cost):
            for each  in cluster_center:
                cluster_center[each] = cluster_center_temp2[each]
            cluster_cost=  temp_sum
            temp_sum = 0
        #进行簇重新分配
        for each in data.index:
            minDist = 10000
            for center in cluster_center:
                dist = np.linalg.norm(data.loc[each].values[0:] - cluster_center[center])
                if (dist < minDist):
                    minDist = dist
                    cluster_record[each] = center
        if(cluster_record==cluster_record_temp):
            tag = 1
        else:
            tag = 0
            for each in cluster_record:
                cluster_record_temp[each] = cluster_record[each]


        #print(cluster_center)
        #print("运行中")
    #print(cluster_record)
    return cluster_record
"""
使用iris数据集 进行K-中心点算法
"""
#读取数据集
data = pd.read_csv("data/iris.csv")
del data[' class']
data_key = []
data_class = []
data_color = []
data = data.apply(lambda x:(x-np.min(x))/(np.max(x)-np.min(x)))
cluster_record = cluster(data,2)
for each in cluster_record:
    print(each,cluster_record[each])
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
