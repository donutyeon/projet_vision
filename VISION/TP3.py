import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("encoded_image.PNG", -1)
if img is None:
        print('image vide')
        exit(0)
img[:,:] = img[:,:]/2
min_ = 255
max_ = 0
h,w = img.shape
for y in range(h):
        for x in range(w):
                if img[y,x] < min_:
                        min_ = img[y,x]
                if img[y,x] > max_:
                        max_ = img[y,x]
imgRes = np.zeros(img.shape, img.dtype)
for y in range(h):
        for x in range(w):
                imgRes[y,x] = (img[y,x]-min_)*255/(max_-min_)
histAvant = np.zeros((256,1),np.uint16)
for y in range(h):
        for x in range(w):
                histAvant[img[y,x]] += 1
histApres = cv2.calcHist([imgRes], [0], None, [256], [0,255])
print((min_, max_))
cv2.imshow("image apres", imgRes)
cv2.imshow("image avtn", img)
plt.figure()
plt.title("image normalisée")
plt.xlabel("niveaux degrés")
plt.ylabel("ND pixel")
plt.plot(histApres)
plt.plot(histAvant)
plt.xlim([0,255])
plt.show()
#cv2.imshow("image hist", histAvant)
cv2.waitKey(0)
cv2.destroyAllWindows()
