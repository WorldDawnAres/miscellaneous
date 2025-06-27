import cv2
import numpy as np
import matplotlib.pyplot as plt
# 读取灰度图像
img = cv2.imread('PythonProgram/1.jpg', 0)
# 绘制直方图和累积分布函数（CDF）
hist, bins = np.histogram(img.flatten(), 256, [0, 256])
cdf = hist.cumsum()
cdf_normalized = cdf * hist.max() / cdf.max()
plt.plot(cdf_normalized, color='b', label='CDF')
plt.hist(img.flatten(), 256, [0, 256], color='r', alpha=0.5, label='Histogram')
plt.xlim([0, 256])
plt.legend()
plt.show()
# 直方图均衡化
equ = cv2.equalizeHist(img)
# 拼接原图和均衡化图像
res = np.hstack((img, equ))
cv2.imshow('Original and Equalized', res)
cv2.waitKey(0)
# 使用CLAHE进行局部直方图均衡化
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)
cv2.imwrite('clahe_2.jpg', cl1)
# 读取彩色图像
img_color = cv2.imread('PythonProgram/1.jpg', 1)
# 分离通道
b, g, r = cv2.split(img_color)
# 分别均衡化
bH = cv2.equalizeHist(b)
gH = cv2.equalizeHist(g)
rH = cv2.equalizeHist(r)
# 合并通道
result = cv2.merge((bH, gH, rH))
# 拼接原图和处理后图像
res_color = np.hstack((img_color, result))
cv2.imshow('Color Histogram Equalization', res_color)
cv2.waitKey(0)
cv2.destroyAllWindows()
