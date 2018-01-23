# coding: utf-8
from scipy.misc import imsave
import numpy as np
from os import mkdir



# 解压缩，返回解压后的字典
def unpickle(file):
    import pickle
    fo = open(file, 'rb')
    dict = pickle.load(fo, encoding='iso-8859-1')
    fo.close()
    return dict


try:
    mkdir('cifar-10-python\\training_img')
    mkdir('cifar-10-python\\test_img')
except OSError:
    pass


# 生成训练集图片，如果需要png格式，只需要改图片后缀名即可。
for j in range(1, 6):
    dataName = "cifar-10-python\\cifar-10-batches-py\\data_batch_" + str(j)  # 读取当前目录下的data_batch12345文件，dataName其实也是data_batch文件的路径，本文和脚本文件在同一目录下。
    Xtr = unpickle(dataName)
    print (dataName + " is loading...")

    for i in range(0, 1000): # 每类训练集个数
        img = np.reshape(Xtr['data'][i], (3, 32, 32))  # Xtr['data']为图片二进制数据
        img = img.transpose(1, 2, 0)  # 读取image
        picName = 'cifar-10-python\\training_img\\' + str(Xtr['labels'][i]) + '_' + str(i + (j - 1)*10000) + '.png'  # Xtr['labels']为图片的标签，值范围0-9，本文中，train文件夹需要存在，并与脚本文件在同一目录下。
        open(picName,'w')
        imsave(picName, img)
        print(imsave)
    print (dataName + " loaded.")

print("test_batch is loading...")

# 生成测试集图片
testXtr = unpickle("cifar-10-python\\cifar-10-batches-py\\test_batch")
for i in range(0, 500): # 每类测试集个数
    img = np.reshape(testXtr['data'][i], (3, 32, 32))
    img = img.transpose(1, 2, 0)
    picName = 'cifar-10-python\\test_img\\' + str(testXtr['labels'][i]) + '_' + str(i) + '.png'
    open(picName,'w')
    imsave(picName, img)
print ("test_batch loaded.")