import cv2
import numpy as np
from random import random, randint   # add any other functions you need here
from KalmanFilter import KalmanFilter

global keep_going
keep_going = True

def detect_inrange(image,surfacemin,surfacemax, lo, hi):
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

def color_picker(image, placement):
    return image[placement[0]][placement[1]]

def game( ):
    KF = KalmanFilter(0.1,[10,10])
    dx = 4 #values with which the ball's pixel x coord increases
    dy = 4 #values with which the ball's pixel y coord increases
 
    x1 = 90 #initial x coord values for ball's top left corner
    x2 = 100 #initial x coord values for ball's bottom right corner
    y1 = 150 #initial y coord values for ball's top left corner
    y2 = 160 #initial y coord values for ball's bottom right corner
    
    x_center_bar = -100
    y_center_bar = -100
    bar_offset = 410         
    cap = cv2.VideoCapture( 0 )

#     while(1):
#         _, frame = cap.read( )
#         frame = cv2.flip(frame, 1,frame)
#         placement = [int(frame.shape[0]/2), int(frame.shape[1]/2)]
#         cv2.circle(frame, (placement[1], placement[0]), 25, (0, 0, 255), 2)
#         image=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#         color =  color_picker(image, placement)
#         cv2.imshow('image',frame)
#         if cv2.waitKey(10)&0xFF==ord('q'):break
#     #cap.release()
#     cv2.destroyAllWindows()

    #cap = cv2.VideoCapture( 0 )
    while( 1 ):
        _, frame = cap.read( )
        height = frame.shape[0]
        width = frame.shape[1]
        frame = cv2.flip(frame, 1,frame)
        # lo = np.array([color[0]-25,color[1]-70,color[2]-70])
        # lo[lo<0] = 0
        # hi = np.array([color[0]+25,color[1]+70,color[2]+70])
        # hi[hi>255] = 255
        # lower_red = np.array([110,50,50]) #lower hsv range of blue colour
        # upper_red = np.array([130,255,255]) #upper hsv range of blue colour
        # lower_red = lo
        # upper_red = hi
        
        #img1,mask,points = detect_inrange(frame,5000,500000, lower_red, upper_red)
        points, rects = detect_visage(frame)
        etat = KF.predict().astype(np.int32)
        #cv2.circle(frame, (int(etat[0]), int(etat[1])), 2, (0,255,0), 5)
        cv2.arrowedLine(frame, (int(etat[0]), int(etat[1])),(int(etat[0]+etat[2]), int(etat[1]+etat[3])), color = (0,255,0), thickness=3, tipLength=0.2)
        if len(points) != 0:
            KF.update(np.expand_dims((points[0][0], points[0][1]), axis = -1))
            circle_x = points[0][0]
            circle_y = points[0][1]
            #circle_rayon=points[0][2]
            #frame = cv2.circle(frame,(circle_x,circle_y),circle_rayon,(100,120,20),5)
            #cv2.rectangle( mask, (circle_x-circle_rayon ,circle_y-circle_rayon) ,(circle_x+circle_rayon ,circle_y+circle_rayon ) ,( 255 ,255 ,0 ) ,2 )
            if rects is not None:
                try:
                    cv2.rectangle(frame, rects[0][0], rects[0][1], (0,0,255), 1, cv2.LINE_AA)
                except: print("error")
                img1 = cv2.rectangle( frame,( x_center_bar-50 ,bar_offset ), ( x_center_bar+50 ,bar_offset+10 ), ( 255 ,255 ,255 ), -1 )
                x_center_bar = int( (circle_x))
            else: x_center_bar=-100
        else: 
            img1 = cv2.rectangle( frame,( x_center_bar-50 ,bar_offset ), ( x_center_bar+50 ,bar_offset+10 ), ( 255 ,255 ,255 ), -1 )
            if int(etat[0]) < 0:
                x_center_bar = 0
            elif int(etat[0]) > width:
                x_center_bar = width
            else:
                x_center_bar = int(etat[0])
       
            #x_center_bar = int(etat[0])
            #print(x_center_bar)
        
        x1 = x1 + dx
        y1 = y1 + dy
        y2 = y2 + dy
        x2 = x2 + dx
        img1 = cv2.circle(frame, (x1, y1), 7, ( 255 ,255 ,255 ), -1)
        #img1 = cv2.rectangle( frame, ( x1 ,y1 ), ( x2 ,y2 ), ( 255 ,255 ,255 ), -1 )
       
        if ( x2 >= width ):
            dx = -(randint(3, 5))
        
        if ( x1-7 <= 0 ):
            dx = randint(3,5)                       
                       
        if ( y1-7 <= 0 ):
            dy = randint(3,5)

        if ( y2 >= bar_offset):
            if (x_center_bar+50 >= x2 and x_center_bar-50  <= x2) or ( x_center_bar+50 >= x1 and x_center_bar-50<= x1):
                dy = -(randint(3, 5))
            if y2 >= height: 
                dy = -(randint(3, 5))

        #cv2.imshow( 'Mask' ,mask )
        cv2.imshow('frame',frame)
        #cv2.imshow('another image',img1)
        #cv2.imshow('Opening',opening)
        #cv2.imshow('Closing',closing)
        #cv2.imshow( 'img' ,img1 )
        k = cv2.waitKey( 5 ) & 0xFF
        if k == 27:
            cap.release( )
            cv2.destroyAllWindows( )
            global keep_going
            keep_going = False
            break
    # while ( 1 ):
    #     if cv2.waitKey( 1 ) & 0xFF == ord( "r" ):
    #         cv2.destroyAllWindows( )
    #         cap.release( )
    #         break
while ( keep_going ):
    game( )
