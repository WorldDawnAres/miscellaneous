import cv2

img_bgr = cv2.imread('PythonProgram/2.jpg')
cv2.imshow('img_bgr', img_bgr)
#roberts算子
roberts_x = cv2.convertScaleAbs(cv2.Sobel(img_bgr, cv2.CV_16S, 1, 0, ksize=3))
roberts_y = cv2.convertScaleAbs(cv2.Sobel(img_bgr, cv2.CV_16S, 0, 1, ksize=3))
roberts = cv2.addWeighted(roberts_x, 0.5, roberts_y, 0.5, 0)

cv2.imshow('roberts', roberts)
#sobel算子
sobel_x = cv2.convertScaleAbs(cv2.Sobel(img_bgr, cv2.CV_16S, 1, 0, ksize=3))
sobel_y = cv2.convertScaleAbs(cv2.Sobel(img_bgr, cv2.CV_16S, 0, 1, ksize=3))
sobel = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)

cv2.imshow('soble', sobel)
#laplace算子
laplace = cv2.Laplacian(img_bgr, cv2.CV_16S, ksize=3)
laplace = cv2.convertScaleAbs(laplace)

cv2.imshow('laplace', laplace)

cv2.waitKey(0)
cv2.destroyAllWindows()