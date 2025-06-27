import cv2
import random
# 1. 加载车牌图像
img = cv2.imread('PythonProgram/3.jpg')
img = cv2.resize(img, (352, 265))
def add_salt_pepper_noise(image, prob):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if random.random() < prob:
                image[i][j] = 255
            elif random.random() < prob:
                image[i][j] = 0
    return image
# 3. 应用四种滤波器
mean = cv2.blur(img, (5, 5))                       # 均值滤波
median = cv2.medianBlur(img, 5)                    # 中值滤波
gaussian = cv2.GaussianBlur(img, (5, 5), 1.5)      # 高斯滤波
box = cv2.boxFilter(img, -1, (5, 5), normalize=True)  # 盒式滤波
# 4. 显示图像（每张图弹窗显示）
cv2.imshow("Original Image", img)
cv2.imshow("Mean Filter", mean)
cv2.imshow("Median Filter", median)
cv2.imshow("Gaussian Filter", gaussian)
cv2.imshow("Box Filter", box)
cv2.imshow("Salt and Pepper Noise", add_salt_pepper_noise(img, 0.02))

cv2.waitKey(0)
cv2.destroyAllWindows()
