import cv2
import numpy as np
from random import random, randint   # add any other functions you need here

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

def game( ):
    dx = 4 #values with which the ball's pixel x coord increases
    dy = 4 #values with which the ball's pixel y coord increases
 
    x1 = 90 #initial x coord values for ball's top left corner
    x2 = 100 #initial x coord values for ball's bottom right corner
    y1 = 150 #initial y coord values for ball's top left corner
    y2 = 160 #initial y coord values for ball's bottom right corner
    
    right_center_bar = -100
    left_center_bar = -100
    bar_offset_right = 570         
    bar_offset_left = 70


    cap = cv2.VideoCapture( 0 )
    while( 1 ):
        _, frame = cap.read( )
        height = frame.shape[0]
        width = frame.shape[1]
        print(width)
        frame = cv2.flip(frame, 1,frame)
        
        lower_orange = np.array([0,150,90]) #lower hsv range of orange colour
        upper_orange = np.array([50,255,200]) #upper hsv range of orange colour

        lower_blue = np.array([110,50,50]) #lower hsv range of blue colour
        upper_blue = np.array([130,255,255]) #upper hsv range of blue colour
        
        img1,mask_orange,points_orange = detect_inrange(frame,200,500000, lower_orange, upper_orange)
        img1,mask_blue,points_blue = detect_inrange(frame,200,500000, lower_blue, upper_blue)
        if len(points_orange) != 0:
            circle_x = points_orange[0][0]
            circle_y = points_orange[0][1]
            circle_rayon=points_orange[0][2]
            frame = cv2.circle(frame,(circle_x,circle_y),circle_rayon,(100,120,20),5)
           
            cv2.rectangle( mask_orange, (circle_x-circle_rayon ,circle_y-circle_rayon) ,(circle_x+circle_rayon ,circle_y+circle_rayon ) ,( 255 ,255 ,0 ) ,2 )
            if(circle_rayon > 50):
                img1 = cv2.rectangle( frame,( bar_offset_left-5 ,left_center_bar-50 ), ( bar_offset_left+5 ,left_center_bar+50 ), ( 255 ,255 ,255 ), -1 )
                left_center_bar = int( (circle_y))
            else: left_center_bar= -100
        
        if len(points_blue) != 0:
            circle_x = points_blue[0][0]
            circle_y = points_blue[0][1]
            circle_rayon=points_blue[0][2]
            frame = cv2.circle(frame,(circle_x,circle_y),circle_rayon,(100,120,20),5)
           
            cv2.rectangle( mask_blue, (circle_x-circle_rayon ,circle_y-circle_rayon) ,(circle_x+circle_rayon ,circle_y+circle_rayon ) ,( 255 ,255 ,0 ) ,2 )
            if(circle_rayon > 50):
                img1 = cv2.rectangle( frame,( bar_offset_right-5 ,right_center_bar-50 ), ( bar_offset_right+5 ,right_center_bar+50 ), ( 255 ,255 ,255 ), -1 )
                right_center_bar = int( (circle_y))
            else: right_center_bar= -100
        
        x1 = x1 + dx
        y1 = y1 + dy
        y2 = y2 + dy
        x2 = x2 + dx
        img1 = cv2.circle(frame, (x1, y1), 7, ( 255 ,255 ,255 ), -1)
        #img1 = cv2.rectangle( frame, ( x1 ,y1 ), ( x2 ,y2 ), ( 255 ,255 ,255 ), -1 )
       
        # if ( x2 >= width ):
        #     dx = -(randint(3, 5))
        
        if ( x1-7 <= 0 ): #wall
            dx = randint(3,5)                       
                       
        if ( y1-7 <= 0 ): #wall
            dy = randint(3,5)
        
        if ( y2 >= height ): #wall
            dy = -(randint(3, 5))

        if ( x2 >= bar_offset_right):
            if (right_center_bar+50 >= y2 and right_center_bar-50  <= y2) or ( right_center_bar+50 >= y1 and right_center_bar-50<= y1):
                dx = -(randint(3, 5))
            if x2 >= width: #wall
                dx = -(randint(3, 5))

        if ( x1 <= bar_offset_left + 10):
            if (left_center_bar+50 >= y2 and left_center_bar-50  <= y2) or ( left_center_bar+50 >= y1 and left_center_bar-50<= y1):
                dx = (randint(3, 5))
            if x1 >= width: #wall
                dx = (randint(3, 5))

        cv2.imshow( 'Mask Orange' ,mask_orange )
        cv2.imshow( 'Mask Blue' ,mask_blue )
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
