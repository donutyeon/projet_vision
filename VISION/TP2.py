import cv2
import numpy as np

img = cv2.imread("VISION\supernova.jpg", cv2.IMREAD_COLOR)
img_b = np.zeros(img.shape, img.dtype)
img_r = np.zeros(img.shape, img.dtype)
img_g = np.zeros(img.shape, img.dtype)
img_gray = np.zeros((img.shape[0], img.shape[1]), img.dtype)

if img is None:
        print('image vide')
        exit(0)

h,w,c = img.shape
'''
for y in range(h):
        for x in range(w):
                img_gray[y,x,0] = np.mean([img[y,x,0], img[y,x,1],img[y,x,2]])
'''
#img_gray = np.mean(img, axis = 2).astype(np.uint8)
img_gray = np.uint8((0.11*img[:,:,0] + 0.59*img[:,:,1]+0.3*img[:,:,2]))
                

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



img_b[:,:,0] = img[:,:,0]
img_g[:,:,1] = img[:,:,1]
img_r[:,:,2] = img[:,:,2]

img_uint16 = np.uint16(img)
img_float32 = np.float32(img)/255

cv2.imshow("image1",img)
cv2.imshow("image1 uint16",img_uint16)
cv2.imshow("image1 float32",img_float32)
cv2.imshow("image1 gray",img_gray)

cv2.imshow("imageRGB",img_rgb)
cv2.imshow("imageHSV",img_hsv)

cv2.imshow("image green",img_g)
cv2.imshow("image blue",img_b)
cv2.imshow("image red",img_r)
cv2.waitKey(0)
cv2.destroyAllWindows()


