import cv2 as cv
import numpy as np
#emeteur=============================
imgA = cv.imread('stardew.png',cv.IMREAD_COLOR)
imgB=np.zeros(imgA.shape,np.uint8)

text='Pipi und kaKi in pIpi cAca laNd 6969 6 9 peepoo              kAKI MEOWMEOMWOEMWOEMW 454545 JSP 752758 BZZZZZZZZZZZZZZZZZZ'
print(text)

texty=np.zeros(len(text)*2,dtype=np.uint8)
for i in range (0,len(text)):
    texty[i]=text.encode()[i]%16
    texty[i+len(text)]=text.encode()[i]//16

cpt=0
for i in range(0,imgB.shape[0]):
    for j in range(0,imgB.shape[1]):
        imgB[i][j][2]=texty[cpt]
        cpt+=1
        if(cpt>len(text)*2-1):
                break

    if(cpt>len(text)-1):
                break                 
imgA=cv.cvtColor(imgA,cv.COLOR_BGR2YCrCb)
imgA=np.uint16(imgA)
imgA=np.array(imgA*256)
for i in range(0,imgB.shape[0]):
    for j in range(0,imgB.shape[1]):
        imgA[i][j][2]+=imgB[i][j][2]*16+1



imgA=cv.cvtColor(imgA,cv.COLOR_YCrCb2BGR)
cv.imwrite('secret.png',imgA)
#repecteur===============
imgA = cv.imread('secret.png',-1)
imgB=np.zeros(imgA.shape,np.uint16)
imgA=cv.cvtColor(imgA,cv.COLOR_BGR2YCrCb)
imgA=np.array(imgA,dtype=np.uint16)
for i in range(0,imgB.shape[0]):
    for j in range(0,imgB.shape[1]):
        imgB[i][j][2]=(np.uint8(imgA[i][j][2])//16)
        imgB[i][j][2]=(np.uint8(imgA[i][j][2])//16)
print("=========================")


text4=[]
for i in range(0,imgB.shape[0]):
    for j in range(0,imgB.shape[1]):
        text4.append(imgB[i][j][2])
text3=[]
for i in range (0,len(text)):
    text3.append(chr(text4[i]+(text4[i+len(text)]*16)))
print(''.join(text3))
