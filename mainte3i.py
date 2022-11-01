import cv2
from restarting import encode,decode
import numpy as np

input_image = "jsp.jpeg"
output_image = "encoded_image.png"
secret_data = 'pipi und kaki in pipi caca land AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
p2='A'
pollo=cv2.imread("pollo.jpg")
imgB=np.zeros(pollo.shape,dtype=np.uint8)
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
# org
height=25
width=20
h,w,c=imgB.shape
org = (0, 20)
org2 =(20,45)
# fontScale
fontScale = 1   
# Blue color in BGR
color = (255, 255, 255)  
# Line thickness of 1 px
thickness = 1

msg_len=len(secret_data)
nb_characters=w//width
i=0
while i < msg_len:    
    if i+nb_characters > msg_len:
        cv2.putText(imgB, secret_data[i:], org, font,fontScale, color, thickness, cv2.LINE_4)
        #string[i-nb_characters:]
    cv2.putText(imgB, secret_data[i:i+nb_characters], org, font,fontScale, color, thickness, cv2.LINE_4)
    org=(org[0],org[1]+height)
    i+=nb_characters

# Using cv2.putText() method
# cv2.putText(imgB, secret_data, org, font,fontScale, color, thickness, cv2.LINE_4)
# cv2.putText(imgB, p2, org2, font,fontScale, color, thickness, cv2.LINE_4)
cv2.imshow("aaa",imgB)
# for letter in secret_data:
#     print(ord(letter))

# print(chr(int('00001101',2)))
# #im = cv2.imread("encoded_image.PNG",-1)
# #cv2.imshow("a",im)
# # encode the data into the image
# encoded_image = encode(img=input_image, message=secret_data)
# # save the output image (encoded image)
# cv2.imwrite(output_image, encoded_image)

# # decode the secret data from the image
# decoded_data = decode(output_image)
# print("[+] Decoded data:", decoded_data)
cv2.waitKey(0)
cv2.destroyAllWindows()

