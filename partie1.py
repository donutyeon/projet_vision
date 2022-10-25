import cv2
import numpy as np

msg="usthb"
imgA=cv2.imread("pollo.jpg",cv2.IMREAD_COLOR)
imgA2=np.zeros(imgA.shape,np.uint16)

img=np.zeros(imgA.shape,np.uint8)
h,w,c=imgA.shape
for y in range(h):
    for x in range(w):
        imgA2[y,x]=imgA[y,x]
imgA2[y,x]=imgA[y,x]*255
i=0
for y in range(h):
    for x in range(w): 
            if(i<len(msg)):
                img[y,x]=ord(msg[i])
                i+=1
img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
cv2.imshow("pollo",imgA2)
cv2.waitKey(0)
cv2.destroyAllWindows()
