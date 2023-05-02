import cv2
import numpy as np

img = cv2.imread("1.jpg")
#初始化seeds项，注意图片长宽的顺序
seeds = cv2.ximgproc.createSuperpixelSEEDS(img.shape[1],img.shape[0],img.shape[2],2000,15,3,5,True)
seeds.iterate(img,10)  #输入图像大小必须与初始化形状相同，迭代次数为10
mask_seeds = seeds.getLabelContourMask()
label_seeds = seeds.getLabels()
number_seeds = seeds.getNumberOfSuperpixels()
mask_inv_seeds = cv2.bitwise_not(mask_seeds)
img_seeds = cv2.bitwise_and(img,img,mask =  mask_inv_seeds)
cv2.imshow("img_seeds",img_seeds)
cv2.waitKey(0)
cv2.destroyAllWindows()
