import cv2
import numpy as np

msg="Ningguang is hot"
img=cv2.imread("pollo.jpg",cv2.IMREAD_COLOR)
hidden_text=np.zeros_like(img)
hidden_text = cv2.putText(hidden_text,msg,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)

#THIS IS JUST TO MAKE TEXT FIH ONE LAYER MESHI 3 TO MAKE IT EASIER
hidden_text=cv2.cvtColor(hidden_text,cv2.COLOR_BGR2GRAY)

#here i chose to work with one value (the third one) and make all the values even numbers
imgYCC = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
for i in range(imgYCC.shape[0]):
    for j in range(imgYCC.shape[1]):
        if imgYCC[i][j][2]%2!=0:
            imgYCC[i][j][2]-=1

#here we encode the text by making that pixel an odd number
for i in range(imgYCC.shape[0]):
    for j in range(imgYCC.shape[1]):
        if hidden_text[i][j]==255:
            imgYCC[i][j][2]+=1


img_encoded=cv2.cvtColor(imgYCC,cv2.COLOR_YCR_CB2BGR)

#decode
imgYCC2=cv2.cvtColor(img_encoded, cv2.COLOR_BGR2YCR_CB)
decoded_msg=np.zeros((imgYCC2.shape[0],imgYCC2.shape[1]))

#when we find an odd number, there's a pixel encoded there (equivalent tae working with last bits)
for i in range(imgYCC2.shape[0]):
    for j in range(imgYCC2.shape[1]):
        if imgYCC2[i][j][2]%2!=0:
            decoded_msg[i][j]=255


cv2.imshow("pollo",img)
cv2.imshow("encoded pollo", img_encoded)
cv2.imshow("decoded msg", decoded_msg)
cv2.waitKey(0)
cv2.destroyAllWindows()