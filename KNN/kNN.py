'''
Created on Sep 16, 2010
kNN: k Nearest Neighbors

Input:      inX: vector to compare to existing dataset (1xN)
            dataSet: size m data set of known vectors (NxM)
            labels: data set labels (1xM vector)
            k: number of neighbors to use for comparison (should be an odd number)
            
Output:     the most popular class label

@author: pbharrin
'''

from numpy import *
import operator
from os import listdir
import imgFmtTra


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]  # numpy.shape[i]返回矩阵ith维的长度
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    # >>> b = [1, 3, 5]
    # >>> tile(b, [2, 3])
    # array([[1, 3, 5, 1, 3, 5, 1, 3, 5],
    #        [1, 3, 5, 1, 3, 5, 1, 3, 5]])
    sqDiffMat = diffMat**2
    # [1, 2] ** 2 = [1, 4]
    sqDistances = sqDiffMat.sum(axis=1)
    # 没有axis参数表示全部相加，axis＝0;表示按列相加，axis＝1;表示按照行的方向相加
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    # argsort函数返回的是数组值从小到大的索引值
    classCount={}  # dict
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
        # dict.get(key, defaut_value=0)
        # key就是dict中的键voteIlabel，如果不存在则返回一个0并存入dict，如果存在则读取当前值并 + 1；
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def str2digit(x):
    if x == 'largeDoses':
        return 3
    if x == 'smallDoses':
        return 2
    if x == 'didntLike':
        return 1

def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file
    returnMat = zeros((numberOfLines,3))        #prepare matrix to return
    classLabelVector = []                       #prepare labels return   
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip() # 去除回车字符
        listFromLine = line.split('\t')  # 按\t分隔
        returnMat[index,:] = listFromLine[0:3] # ( i >= 0 and i < 3)
        classLabelVector.append(str2digit(listFromLine[-1]))  # 负数表示，从后面倒数的索引 -1 为倒数第一个
        index += 1
    return returnMat,classLabelVector

# 归一化
def autoNorm(dataSet):
    minVals = dataSet.min(0) # 0表示返回每列的最小值，而不是行
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))   #element wise divide
    return normDataSet, ranges, minVals
   
def datingClassTest():
    hoRatio = 0.50      #hold out 10%
    datingDataMat,datingLabels = file2matrix('datingTestSet.txt')       #load data setfrom file
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print("the classifier came back with: %d, the real answer is: %d"%(classifierResult, datingLabels[i]))
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print("the total error rate is: %f" % (errorCount/float(numTestVecs)))
    print(errorCount)
    
def txt2vector(filename, size):
    returnVect = zeros((1,size**2))
    fr = open(filename)
    for i in range(size):
        lineStr = fr.readline().split(' ')
        for j in range(size):
            returnVect[0, size*i+j] = int(lineStr[j])
    return returnVect

def img2vector(filename,size):
    returnVect = zeros((1,size**2))
    data = imgFmtTra.img2pixel(filename,size)
    for i in range(size):
        for j in range(size):
            returnVect[0,size*i+j] = data[i,j]
    return returnVect


def knnClassTestWithTxt(trainpath,testpath,size, k):
    hwLabels = []
    trainingFileList = listdir(trainpath)  # load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m, size ** 2))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]  # take off .png
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i, :] = txt2vector('%s/%s' % (trainpath, fileNameStr), size)
    testFileList = listdir(testpath)  # iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]  # take off .png
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = txt2vector('%s/%s' % (testpath, fileNameStr), size)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, k)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr))
        if (classifierResult != classNumStr): errorCount += 1.0
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total error rate is: %f" % (errorCount / float(mTest)))


def knnClassTestWithImg(trainpath,testpath,size, k):
    hwLabels = []
    trainingFileList = listdir(trainpath)           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m,size**2))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .png
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('%s/%s' %(trainpath,fileNameStr),size)
    testFileList = listdir(testpath)        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .png
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('%s/%s' %(testpath, fileNameStr),size)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, k)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr))
        if (classifierResult != classNumStr): errorCount += 1.0
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total error rate is: %f" % (errorCount/float(mTest)))


# if __name__ == '__main__':
#     # group,lables = createDataSet()
#     # print(group)
#     # print(lables)
#     # e = eye(3)
#     # print(e.shape)
#     # print(e.shape[1])
#     # print(int('didntLike'))
#     # returnMat, classLabelVector=file2matrix('datingTestSet.txt')
#     # print(returnMat)
#     # print(classLabelVector)
#     # print(autoNorm(returnMat))
#     # datingClassTest()
