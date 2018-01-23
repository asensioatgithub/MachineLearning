from sklearn.datasets import load_digits
import numpy as np
import kNN
from PIL import Image

def sklearnDigitsTest():
    digits = load_digits()
    print(digits.keys())

    np.random.seed(2)
    data = digits.data
    # print(len(data))
    # print(data[0,:])
    labels = digits.target
    print(len(labels))
    indices = np.random.permutation(len(data))
    # 用来产生一个随机序列作为索引，再使用这个序列从原来的数据集中按照新的随机顺序产生随机数据集。
    train_data = data[indices[:-297]]       # 随机选取1500个样本作为训练数据集
    train_label = labels[indices[:-297]]    # 并且选取这1500个样本的标签作为训练数据集的标签
    test_data = data[indices[-297:]]        # 剩下的297个样本作为测试数据集
    test_label = labels[indices[-297:]]
    errorCount = 0.0
    mTest = len(test_data)
    for i in range(297):
        classifierResult = kNN.classify0(test_data[i], train_data, train_label, 5)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, test_label[i]))
        if (classifierResult != test_label[i]): errorCount += 1.0
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total error rate is: %f" % (errorCount / float(mTest)))

    print("eg. the 1st  image:")
    print(digits.images[0])  # 8*8pixel
    imgMat = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            imgMat[i, j] = int(data[0,8*i+j])
    im = Image.fromarray(imgMat)
    im.show()

