import kNN
import time
import imgFmtTra
from os import mkdir
import numpy as np
import sklearnDigit as sd


if __name__ == '__main__':

    handwriting_trainImgs_path = 'imgs\\training_img'
    handwriting_trainTxts_path = 'imgs\\training_txt'
    handwriting_testImgs_path = 'imgs\\test_img'
    handwriting_testTxts_path = 'imgs\\test_txt'

    cifar_trainImgs_path = 'cifar-10-python\\training_img'
    cifar_trainTxts_path = 'cifar-10-python\\training_txt'
    cifar_testImgs_path = 'cifar-10-python\\training_img'
    cifar_testTxts_path = 'cifar-10-python\\test_txt'
    try:
        mkdir(cifar_testTxts_path)
        mkdir(cifar_trainTxts_path)
        mkdir(handwriting_testTxts_path)
        mkdir(handwriting_trainTxts_path)
    except OSError:
        pass


    '''
    transform image to pixel array: 
    '''

    # print("processing...")
    # start = time.clock()

    # imgFmtTra.img2txt(cifar_trainImgs_path, cifar_trainTxts_path, 32) # pixel:32*32
    # imgFmtTra.img2txt(cifar_testImgs_path, cifar_testTxts_path, 32)
    # imgFmtTra.img2txt(cifar_trainImgs_path, cifar_trainTxts_path, 64) # pixel:32*32
    # imgFmtTra.img2txt(cifar_testImgs_path, cifar_testTxts_path, 64)

    imgFmtTra.img2txt(handwriting_trainImgs_path, handwriting_trainTxts_path, 32)   # pixel:32*32
    imgFmtTra.img2txt(handwriting_testImgs_path, handwriting_testTxts_path, 32)

    # imgFmtTra.img2txt(handwriting_trainImgs_path, handwriting_trainTxts_path, 64)  # pixel:64*64
    # imgFmtTra.img2txt(handwriting_testImgs_path, handwriting_testTxts_path, 64)
    # end = time.clock()
    # print("time:"+ end-start)

    '''
    transform pixel array to image: 
        def pixel2img(txtPath, imgPixel)
    '''
    # txt_path = 'imgs\\training_txt\\0_0.txt'
    # imgFmtTra.pixel2img(txt_path, 64)


    '''
    datingt test:
        def datingClassTest()
    '''
    # start = time.clock()
    # kNN.datingClassTest()
    # end = time.clock()
    # print("time:"+ end-start)

    '''
    handwritingdigits test: 
        def knnClassTestWithImg(trainingPath, testPath, imgPixel, KNN-K)
    '''
    # start = time.clock()
    # kNN.knnClassTestWithImg(handwriting_trainImgs_path, handwriting_testImgs_path, 64, 6)
    # kNN.knnClassTestWithTxt(handwriting_trainTxts_path, handwriting_testTxts_path, 64 ,6)
    # end = time.clock()
    # print("time:"+ end-start)

    '''
    CIFAR_10 test:
        def knnClassTestWithImg(trainingPath, testPath, imgPixel, KNN-K)
    '''
    # print("processing...")
    # start = time.clock()
    # kNN.knnClassTestWithImg(cifar_trainImgs_path, cifar_testImgs_path, 64 ,5)
    # kNN.knnClassTestWithTxt(cifar_trainTxts_path, cifar_testTxts_path, 64, 5)
    # end = time.clock()
    # print("time:"+ end-start)


    '''
    sklearn-digit test: 
        (sklearn-digits: 1797个样本，每个样本包括8*8像素的图像和一个[0, 9]整数的标签)
        dict_keys(['data', 'target', 'target_names', 'images', 'DESCR'])
        
        data:           ndarray类型，将images按行展开成一行，共有1797行
        target:         ndarray类型，指明每张图片的标签，也就是每张图片代表的数字
        target_names:   ndarray类型，数据集中所有标签值
        images:         ndarray类型，保存8*8的图像，里面的元素是float64类型，共有1797张图片
        DESCR:          数据集的描述，作者，数据来源等
    '''
    #sd.sklearnDigitsTest()


