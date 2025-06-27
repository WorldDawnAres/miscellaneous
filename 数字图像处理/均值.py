import cv2  as cv
import numpy as np
 
def cv_show(name, img):
    cv.imshow(name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()
 
# 在图片上生成椒盐噪声
def add_peppersalt_noise(image, n=10000):
    result = image.copy()
    # 测量图片的长和宽
    w, h =image.shape[:2]
    # 生成n个椒盐噪声
    for i in range(n):
        x = np.random.randint(1, w)
        y=  np.random.randint(1, h)
        if np.random.randint(0, 2) == 0 :
            result[x, y] = 0
        else:
            result[x,y] = 255
    return result
 
# 在图片上生成高斯噪声
def add_gauss_noise(image, mean=0, val=0.01):
    size = image.shape
    image = image / 255
    gauss = np.random.normal(mean, val**0.05, size)
    image = image + gauss
    return image
 
# blur均值滤波，对高斯噪声有较好的去除效果，对象可以是彩色图像和灰度图像
img = cv.imread('PythonProgram/1.jpg')
if img is None:
    print('Failed to read the image')
 
img1 = add_peppersalt_noise(img)
cv_show('img', img1)
 
# 默认为规定尺寸的1/n的全1矩阵
img2 = cv.blur(img1, (3, 3))
cv_show('img2', img2)
 
img3 = cv.blur(img1, (5, 5))
cv_show('img3', img3)
