import cv2  as cv
import numpy as np
 
def cv_show(name, img):
    cv.imshow(name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()
def add_gauss_noise(image, mean=0, val=0.01):
    size = image.shape
    # 对图像归一化处理
    image = image / 255
    gauss = np.random.normal(mean, val**0.05, size)
    image = image + gauss
    return image
 
img = cv.imread('PythonProgram/1.jpg')
if img is None:
    print('Failed to read the image')
 
img1 = add_gauss_noise(img)
cv_show('img1', img1)
 
img2 = cv.GaussianBlur(img1, (3, 3), 1, 2)
cv_show('img2', img2)