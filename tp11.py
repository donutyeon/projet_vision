import cv2
import numpy as np
from KalmanFilter import KalmanFilter

def detect_visage(image):
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
        points = []
        rects = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors =3)
        for x, y, w, h in face:
                points.append(np.array([int(x+w/2), int(y+h/2)]))
                rects.append(np.array([(x,y), (x+w, y+h)]))
        return points, rects

lo = np.array([  0, 156,  37]) #lower hsv range of blue colour
hi = np.array([ 36, 255, 177])
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
KF = KalmanFilter(0.1,[10,10])
while(True):
    ret,frame=VideoCap.read()
    cv2.flip(frame,1,frame)
    image,mask,points=detect_inrange(frame,5000,50000)

    etat = KF.predict().astype(np.int32)
    cv2.circle(frame, (int(etat[0]), int(etat[1])), 2, (0,255,0), 5)
    cv2.arrowedLine(frame, (int(etat[0]), int(etat[1])),(int(etat[0]+etat[2]), int(etat[1]+etat[3])), color = (0,255,0), thickness=3, tipLength=0.2)
    #points, rects = detect_visage(frame)
    if len(points) != 0:
        KF.update(np.expand_dims((points[0][0], points[0][1]), axis = -1))
        circle_x = points[0][0]
        circle_y = points[0][1]
        circle_rayon=points[0][2]
        cv2.circle(frame,(circle_x,circle_y),circle_rayon,(200,255,20),3)
    # if rects is not None:
    #     try:
    #         print(rects[0])
    #         cv2.rectangle(frame, rects[0][0], rects[0][1], (0,0,255), 1, cv2.LINE_AA)
    #     except: print("error")
    if mask is not None :
        cv2.imshow("mask",mask)
   
    #print(image[100,100])
    cv2.imshow('image',frame)
    if cv2.waitKey(10)&0xFF==ord('q'):break
VideoCap.release()
cv2.destroyAllWindows()

