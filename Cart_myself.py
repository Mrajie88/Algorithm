import numpy as np
import pandas as pd

#递归创建决策二叉树
def createTree(data,labels,decFeature):
    Tree  = []
#确定决策树终止条件
    if len(data)< 1:
        #print(data)
        return
    if len(labels)<1:
        return data[decFeature]
    if(len(data[decFeature].values)==1):
        return list(set(data[decFeature].values))
    split_label,split_value =best_spilt_data(data,labels,decFeature)
#将数据进行二分化
    split_data1 = data[data[split_label]==split_value]
   # print(split_data1)
   # del split_data1[split_label]
    labels1 = np.copy(labels).tolist()
    labels1.remove(split_label)
    Tree.append([str(split_label)+"="+str(split_value),createTree(split_data1,labels1,decFeature)])
    split_data2 = data[data[split_label]!=split_value]
    Tree.append([str(split_label)+"!="+str(split_value),createTree(split_data2,labels,decFeature)])
#创建二叉树
    return Tree
#规约数据
def recData(data,fec,decFeacture):
    recdata = data[[fec,decFeature]]
    return recdata
#计算基尼指数
def calGini(data,col,unique_val):
    dis = (data[col].value_counts()/len(data)).tolist()
    mingini = 1000
    gini = 1.0
    for i in range(len(dis)):
        gini+=dis[i]*calGini2(data,i+1,col,unique_val)
        if(gini<mingini):
            mingini = gini
    return mingini,i+1
def calGini2(data,i,col,unique_val):
    record = {}
    for each in unique_val:
        record[each] = 0
    recdata = data[data[col]==i]
    gini = 1.0
    for j in recdata.index:
        record[recdata.loc[j,decFeature]]+=1
    for each in record:
        if(record[each]!=0):
            prob = (record[each]/len(recdata))**2
            gini-=prob
    return gini
#选择最好的划分方式
def best_spilt_data(data,labels,decFeature):
    minGini = 1000
    split_label = decFeature
    split_value = 0
    for each in labels:
        recdata = recData(data,each,decFeature)
        unique_val = recdata.drop_duplicates(decFeature)[decFeature].tolist()
        Gini,temp = calGini(recdata,each,unique_val)
        if Gini<minGini:
            minGini = Gini
            split_label = each
            split_value = temp
    #print(minGini)
    #print(split_label)
    #print(split_value)
    return split_label,split_value
def DrawTree(Tree):
    if(Tree is None): return
    if(len(Tree)<2): return Tree
    for each in Tree:
        print(each[0])
        if(each[1] is not None):
            print(DrawTree(each[1]))
#需要将决策属性放到右列第一行
data = pd.read_csv("data/balance-scale.csv")
labels = data.columns.values[:].tolist()
decFeature = labels[-1]
labels = labels[:-1]
Tree = createTree(data,labels,decFeature)
#绘制二叉树
DrawTree(Tree)

