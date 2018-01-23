from numpy import *
from os import listdir
from zhon.hanzi import punctuation  # 中文标点
import xlrd                         # 处理excel文件
import re
import random as rd
import bayes as nb                  # 贝叶斯API
import jieba
import jieba.analyse
import jieba.posseg as pseg
'''
jieba分词module, 在anaconda prompt用pip install jieba安装
'''

def read_xls_file(fileStr):
    xls_data = xlrd.open_workbook(r"data/%s"%fileStr)
    table = xls_data.sheet_by_index(0)
    return table

def getWordList(table,i):
    # 加载停用词表
    stoplist = [line.strip() for line in open('stopword.txt').readlines()]
    wordlist = []
    # 去除中文标点和无关字符
    comment = re.sub(r"[%s]"%punctuation, '', (''.join(table.row_values(i))).replace('\n','').replace(' ','').replace('/',''))
    # print(comment)
    # 分词
    # result = jieba.cut(comment, cut_all=True)         # 全模式
    # result = pseg.cut(comment)                        # 词性标注，标注句子分词后每个词的词性
    result = jieba.cut(comment)                         # 默认是精准模式
    # result = jieba.analyse.extract_tags(comment, 2)   # 提取关键词
    # 去除停用词，如“是”“的”“啊”等
    segs = [word for word in list(result)]
    segs = [word for word in list(segs) if word not in stoplist]
    for t in segs:
        wordlist.append(t)
    return wordlist

def test1():
    docList = []; classList = []
    tablePOS = read_xls_file("CHENGFENGPOLANGPOS.xls")
    # print(tablePOS.nrows) # CHENGFENGPOLANGPOS.xls有4000条评论
    tableNEG = read_xls_file("CHENGFENGPOLANGNEG.xls")
    # print(tablePOS.nrows) # CHENGFENGPOLANGNEG.xls有4000条评论
    # resultList = rd.sample(range(0, 4001), 1000)  # sample(x,y)函数的作用是从序列x中，随机选择y个不重复的元素。
    # 生成词表
    for i in range(4000):
    #     wordlist = []
        Index = int(random.uniform(0, 4000)) #产生一个0~4000的随机数作为
        classList.append(0)
        wordList = getWordList(tablePOS, Index)
        docList.append(wordList)
        wordList = getWordList(tableNEG, Index)
        classList.append(1)
        docList.append(wordList)
    print("The classlist is:\n", classList)
    print("The doclist is:\n", docList)
    vocabList = nb.createVocabList(docList)  # create vocabulary
    print("The vocabList:\n", vocabList)
    '''
    训练
    '''
    vocabList = nb.createVocabList(docList)  # create vocabulary
    trainingSet = list(range(8000));
    testSet = []  # create test set
    for i in range(1000):# 随机选取1000条评论作为测试集，7000条作为训练集
        randIndex = int(random.uniform(0, len(trainingSet)))  # uniform() 方法将随机生成下一个实数，它在[x,y]范围内
        testSet.append(trainingSet[randIndex])
        del (trainingSet[randIndex])
    trainMat = [];
    trainClasses = []
    for docIndex in trainingSet:  # train the classifier (get probs) trainNB0
        trainMat.append(nb.bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = nb.trainNB0(array(trainMat), array(trainClasses))
    # print(p0V, p1V)
    '''
    测试
    '''
    errorCount = 0
    for docIndex in testSet:  # classify the remaining items
        wordVector = nb.bagOfWords2VecMN(vocabList, docList[docIndex])
        answr = nb.classifyNB(array(wordVector), p0V, p1V, pSpam)
        if  answr != classList[docIndex]:
            errorCount += 1
            print("classfied as %d, classification error"%answr, docList[docIndex])
        else:
            print("classfied as %d, classification correctly"%answr, docList[docIndex])
    print('1: NEG, 0: POS')
    print('the error rate is: ', float(errorCount) / len(testSet))




def test2():
    docList = [];
    classList = []
    tablePOS = read_xls_file("CHENGFENGPOLANGPOS.xls")
    # print(tablePOS.nrows) # CHENGFENGPOLANGPOS.xls有4000条评论
    tableNEG = read_xls_file("CHENGFENGPOLANGNEG.xls")
    # print(tablePOS.nrows) # CHENGFENGPOLANGNEG.xls有4000条评论
    # 生成词表
    for i in range(tablePOS.nrows):
        classList.append(0)
        wordList = getWordList(tablePOS, i)
        docList.append(wordList)
        wordList = getWordList(tableNEG, i)
        classList.append(1)
        docList.append(wordList)
    print("The classlist is:\n", classList)
    print("The doclist is:\n", docList)
    vocabList = nb.createVocabList(docList)  # create vocabulary
    print("The vocabList:\n", vocabList)
    '''
    训练
    '''
    trainMat = []; trainClasses = []
    # for docIndex in trainingSet:#train the classifier (get probs) trainNB0
    count = tablePOS.nrows + tableNEG.nrows
    for docIndex in range(count):
        trainMat.append(nb.bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pNeg = nb.trainNB0(array(trainMat), array(trainClasses))
    print("积极评论的条件概率：", p0V)
    print("消极评论的条件概率：", p1V)
    print(pNeg)

    '''
    测试
    '''
    errorCount = 0
    tableTEST = read_xls_file("CHENGFENGPOLANGTEST.xls")
    # print(tableTEST.nrows)
    errorCount = 0
    for i in range(tableTEST.nrows):
        wordList = getWordList(tableTEST, i)
        print(tableTEST.row_values(i))
        wordVector = nb.bagOfWords2VecMN(vocabList, wordList)
        answr = nb.classifyNB(array(wordVector), p0V, p1V, pNeg)
        # print(answr)
        if i<425: # 目测CHENGFENGPOLANGTEST.xls中前425条为消极评论
            if  answr == 1:
                print("classfied as Neg, classification correctly")
            else:
                print("classfied as Neg, classification error")
                errorCount += 1
        else:
            if  answr == 0:
                print("classfied as Pos, classification correctly")
            else:
                print("classfied as Pos, classification error")
                errorCount += 1

    print('the error rate is: ', float(errorCount) / tableTEST.nrows)
    print('1: NEG, 0: POS')


if __name__ == '__main__':

    # nb.testingNB()
    # nb.spamTest()

    '''
    1.test by partition POS.xls and NEG.xls with 1/7(test/train)
    '''
    # test1()

    '''
    2.test with CHENGFENGPOLANGTEST.xls
    '''
    test2() # error rate: 0.145
