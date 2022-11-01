import cv2

img=cv2.imread('pollo.jpg')
img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

print(img2)