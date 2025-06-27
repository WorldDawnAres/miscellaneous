import cv2
# 1. 读取原图
img_bgr = cv2.imread('PythonProgram/3.jpg')
img_bgr= cv2.resize(img_bgr, (352, 265))
# 2. 转换为 RGB
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
# 3. 转换为灰度图像
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
# 4. 转换为 HSV 图像
img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
# 5. 显示图像
cv2.imshow('Original Image', img_bgr)
cv2.imshow('Grayscale Image', img_gray)
cv2.imshow('HSV Image', img_hsv)
# 6. 等待用户按任意键关闭所有窗口
cv2.waitKey(0)
cv2.destroyAllWindows()
