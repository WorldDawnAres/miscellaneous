import cv2  as cv
import numpy as np
def cv_show(name, img):
    cv.imshow(name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()

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
 
 
img = cv.imread('PythonProgram/1.jpg')
if img is None:
    print('Failed to read the image')
 
img1 = add_peppersalt_noise(img)
cv_show('img', img1)
 
# 中值滤波，可对灰色图像和彩色图像使用
img2 = cv.medianBlur(img1, 3)
cv_show('img2', img2)
# ksize变大图像变模糊
img3 = cv.medianBlur(img1, 9)
cv_show('img3', img3)