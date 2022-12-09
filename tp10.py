import cv2
import numpy as np
# lo=np.array([90,100,70])
# hi=np.array([120,170,140])

lo = np.array([0,50,120]) #lower hsv range of blue colour
hi = np.array([70,120,200])
def detect_inrange(image,surfacemin,surfacemax):
    points=[]
    image=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(image,lo,hi)
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)
    elements = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    elements = sorted(elements,key = lambda x:cv2.contourArea(x), reverse=True)
    for element in elements:
        if cv2.contourArea(element) > surfacemin and cv2.contourArea(element) < surfacemax:
            ((x,y),rayon)=cv2.minEnclosingCircle(element)
            points.append(np.array([int(x),int(y),int(rayon)]))
        else:
            break
    return image,mask,points


VideoCap=cv2.VideoCapture(0)

while(True):
    ret,frame=VideoCap.read()
    cv2.flip(frame,1,frame)
    image,mask,points=detect_inrange(frame,200,5000)
    if len(points) != 0:
        circle_x = points[0][0]
        circle_y = points[0][1]
        circle_rayon=points[0][2]
        cv2.circle(image,(circle_x,circle_y),circle_rayon,(200,120,20),15)
    if mask is not None :
        cv2.imshow("mask",mask)
   
    print(image[100,100])
    cv2.imshow('image',image)
    if cv2.waitKey(10)&0xFF==ord('q'):break
VideoCap.release()
cv2.destroyAllWindows()
