import cv2
import numpy as np

img3 = np.random.randn(500,500)
img = cv2.imread("VISION\supernova.jpg", cv2.IMREAD_COLOR)
img2 = np.zeros((838,838), dtype=np.float32)
if img is None:
        print('image vide')
        exit(0)

h,w,c = img.shape
imgRes = np.zeros(img.shape, img.dtype)

# for p in range(c):
#         for y in range(h):
#                 for x in range(w):
#                         imgRes[y,x,p] = img[y,x,p]/255
imgRes = 255 - img
cv2.imwrite("negative_nebula.png", imgRes)
print(type(img))
print(img.dtype)
cv2.imshow("image1", img)
cv2.imshow("negative", imgRes)
# cv2.imshow("image2", img2)
# cv2.imshow("image3", img3)
print((h,w))
cv2.waitKey(0)
cv2.destroyAllWindows()
