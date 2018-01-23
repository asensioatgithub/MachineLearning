from PIL import Image
import numpy as np
from os import listdir


def img2txt(imgs_path,txts_path,size):
    """
    将图像数据转换为txt文件
    :param img_path: 图像文件路径
    """
    FileList = listdir(imgs_path)
    m = len(FileList)
    for i in range(m):
        fileNameStr = FileList[i]
        fileStr = fileNameStr.split('.')[0]  # take off .txt
        txtfile = open("%s\\%s.txt"%(txts_path,fileStr), 'w')
        filepath=imgs_path+"\\"+fileNameStr
        im = Image.open(filepath).convert('L').resize((size, size))  # type:Image.Image # 1:转化为二值化图; L:灰度图
        data = np.asarray(im,'i')

        np.savetxt(txtfile, data, fmt='%i', delimiter=' ')
        # print(data[0:10,:])
        # for j in range(size):
        #     # print(data[j,:])
        #     txtfile.write(str(data[j,:]).replace('[','').replace(']',''))
        #     # txtfile.write('\n')
        txtfile.close()


def img2pixel(img_path,size):
    """
    :param img_path: 图像文件路径
    """
    im = Image.open(img_path).convert('L').resize((size, size))  # type:Image.Image
    data = np.asarray(im)
    # print(data[0:10,:])
    return data


def pixel2img(txt_path,size):
    img_file = open(txt_path,'r')
    # a = np.loadtxt(img_path)
    imgMat = np.zeros((size,size))
    for i in range(size):
        line = img_file.readline()
        temp = line.split(' ')
        for j in range(size):
            imgMat[i,j] = int(temp[j])
    im = Image.fromarray(imgMat)
    im.show(im)
    # im.save("your_file.png")


