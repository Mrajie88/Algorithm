# -*- coding: utf-8 -*-


from numpy import *
import numpy as np
import pandas as pd
import operator


# 计算数据集的基尼指数
def calcGini(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    # 给所有可能分类创建字典
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    print(labelCounts)
    Gini = 1.0
    # 计算GiNi指数
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        Gini -= prob * prob
    return Gini


# 数据规约 对数据进行axis列取出value值
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

# 选择最好的数据集划分方式
def chooseBestFeatureToSplit(dataSet, labels):
    #print(labels)
    numFeatures = len(dataSet[0]) - 1
    bestGiniIndex = 100000.0
    bestFeature = -1
    bestSplitDict = {}
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        #print(featList)
        # 对离散型特征进行处理

        uniqueVals = set(featList)
        #print(uniqueVals)
        newGiniIndex = 0.0
            # 计算该特征下每种划分的信息熵
        for value in uniqueVals:
         subDataSet = splitDataSet(dataSet, i, value)
         prob = len(subDataSet) / float(len(dataSet))
         newGiniIndex += prob * calcGini(subDataSet)
         GiniIndex = newGiniIndex
        if GiniIndex < bestGiniIndex:
            bestGiniIndex = GiniIndex
            bestFeature = i
   # print(bestFeature)
    return bestFeature


# 特征若已经划分完，节点下的样本还没有统一取值，则需要进行投票
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    return max(classCount)


# 主程序，递归产生决策树
def createTree(dataSet, labels, data_full, labels_full):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet, labels)
   # print(bestFeat)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    if type(dataSet[0][bestFeat]).__name__ == 'str':
        currentlabel = labels_full.index(labels[bestFeat])
        featValuesFull = [example[currentlabel] for example in data_full]
        uniqueValsFull = set(featValuesFull)
    del (labels[bestFeat])
    # 针对bestFeat的每个取值，划分出一个子树。
    for value in uniqueVals:
        subLabels = labels[:]
        if type(dataSet[0][bestFeat]).__name__ == 'str':
            uniqueValsFull.remove(value)
        myTree[bestFeatLabel][value] = createTree(splitDataSet \
                                                      (dataSet, bestFeat, value), subLabels, data_full, labels_full)
    if type(dataSet[0][bestFeat]).__name__ == 'str':
        for value in uniqueValsFull:
            myTree[bestFeatLabel][value] = majorityCnt(classList)
    return myTree


df = pd.read_csv('data/balance-scale.csv')
data = df.values[:625, :].tolist()
data_full = data[:]
labels = df.columns.values[:].tolist()
labels_full = labels[:]
myTree = createTree(data, labels, data_full, labels_full)

