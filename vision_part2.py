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

def color_picker(image, placement):
    return image[placement[0]][placement[1]]

def game( ):
    dx = 4 #values with which the ball's pixel x coord increases
    dy = 4 #values with which the ball's pixel y coord increases
 
    x1 = 90 #initial x coord values for ball's top left corner
    x2 = 100 #initial x coord values for ball's bottom right corner
    y1 = 150 #initial y coord values for ball's top left corner
    y2 = 160 #initial y coord values for ball's bottom right corner
    
    x_center_bar = -100
    y_center_bar = -100
    bar_offset = 410
    x_brick_dimension = 30
    y_brick_dimension = 10
    f=0
    bricks = []

    for i in range(4):
        bricks.append([])
     
        for j in range(18):
            bricks[i].append([])
             
        for j in range(18):
            x9 = (x_brick_dimension-26) + 40*j
        
            y9 = y_brick_dimension + 20*(i+2)
            
            bricks[i][j] = str(x9)+"_"+str(y9)
          


    cap = cv2.VideoCapture( 0 )

    while(1):
        _, frame = cap.read( )
        frame = cv2.flip(frame, 1,frame)
        placement = [int(frame.shape[0]/2), int(frame.shape[1]/2)]
        color_bgr =  color_picker(frame, placement)
        cv2.circle(frame, (placement[1], placement[0]), 25, (int(color_bgr[0]), int(color_bgr[1]), int(color_bgr[2])), 2)
        image=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        color =color_picker(image, placement)
        cv2.imshow('image',frame)
        if cv2.waitKey(10)&0xFF==ord('q'):break
    #cap.release()
    cv2.destroyAllWindows()

    global keep_going
    while( keep_going ):
        _, frame = cap.read( )
        height = frame.shape[0]
        width = frame.shape[1]
        frame = cv2.flip(frame, 1,frame)
        lo = np.array([color[0]-25,color[1]-70,color[2]-70])
        lo[lo<0] = 0
        hi = np.array([color[0]+25,color[1]+70,color[2]+70])
        hi[hi>255] = 255
        # lower_red = np.array([110,50,50]) #lower hsv range of blue colour
        # upper_red = np.array([130,255,255]) #upper hsv range of blue colour
        # print(lo, hi)
        lower_red = lo
        upper_red = hi
        
        
        img1,mask,points = detect_inrange(frame,200,500000, lower_red, upper_red)
        if len(points) != 0:
            circle_x = points[0][0]
            circle_y = points[0][1]
            circle_rayon=points[0][2]
            frame = cv2.circle(frame,(circle_x,circle_y),circle_rayon,(int(color_bgr[0]),int(color_bgr[1]),int(color_bgr[2])),5)
            cv2.rectangle( mask, (circle_x-circle_rayon ,circle_y-circle_rayon) ,(circle_x+circle_rayon ,circle_y+circle_rayon ) ,( 255 ,255 ,0 ) ,2 )
            if(circle_rayon > 50):
                img1 = cv2.rectangle( frame,( x_center_bar-50 ,bar_offset ), ( x_center_bar+50 ,bar_offset+10 ), ( 255 ,255 ,255 ), -1 )
                x_center_bar = int( (circle_x) )
            else: x_center_bar= -100
        
        x1 = x1 + dx
        y1 = y1 + dy
        y2 = y2 + dy
        x2 = x2 + dx
        img1 = cv2.circle(frame, (x1, y1), 7, ( 255 ,255 ,255 ), -1)
        #img1 = cv2.rectangle( frame, ( x1 ,y1 ), ( x2 ,y2 ), ( 255 ,255 ,255 ), -1 )
        a = random()
        number_of_bricks = int(width/(x_brick_dimension+10))
        #print(number_of_bricks)
        for i in range(4):
            for j in range(number_of_bricks):
                
                rec = bricks[i][j]                    
                if rec != []:
                    rec1 = str(rec)

                    rec_1 = rec1.split("_")
    
                    x12 = int(rec_1[0])
                    y12 = int(rec_1[1])
           
                
                img1 = cv2.rectangle( frame, ( x12 , y12 ), ( x12+x_brick_dimension , y12+y_brick_dimension ), ( 210 ,90+(10*j) ,110+(20*j) ), -1 )
        
        if ( x2 >= width ):
            dx = -(randint(3, 5))
            
            
        for i in range(4):
            for j in range(number_of_bricks):
                ree = bricks[i][j]
                if ree != []:
                    ree1 = str(ree)
                    ree_1 = ree1.split("_")
                    x13 = int (ree_1[0])
                    y13 = int (ree_1[1])
                    #works but to revise psk telfetli
                    if (((x13 <= x2 and x13+x_brick_dimension >=x2) or (x13 <= x1 and x13+x_brick_dimension >=x1)) and y1-7<=y13+y_brick_dimension ) or (y1+7<=y_brick_dimension):
                        dy = randint(3,5)
                        bricks[i][j]=[]
                        f = f+1
                        break                       
                       
                         
 
        if ( x1 <= 0 ):
            dx = randint(3,5)
        if ( y2 >= bar_offset and  y2 < bar_offset+10 ):
            if (x_center_bar+50 >= x2 and x_center_bar-50  <= x2) or ( x_center_bar+50 >= x1 and x_center_bar-50<= x1):
                dy = -(randint(3, 5))
        if y1 > bar_offset:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = ( 230 ,25 )
            fontScale              = 1
            fontColor              = ( 255 ,255 ,255 )
            lineType               = 2
            

            cv2.putText( img1 ,'GAME OVER!' ,bottomLeftCornerOfText ,font ,fontScale ,fontColor ,lineType )        
            if y2 > bar_offset+60:
                while(1):
                    #cv2.imshow('frame',frame)
                    k = cv2.waitKey(5) & 0xFF
                    if k == 27:
                        cv2.destroyAllWindows()
                        cap.release()
                        keep_going = False
                        break
                # cv2.destroyAllWindows( )
                # cap.release( )
                # break
        else: 
            score = "SCORE : "+str(f)
            font = cv2.FONT_HERSHEY_SIMPLEX
                
            bottomLeftCornerOfText = ( 230 ,25 )
            fontScale              = 1
            fontColor              = ( 210 ,120 ,120 )
            lineType               = 2
            cv2.putText( img1 ,score,bottomLeftCornerOfText ,font ,fontScale ,fontColor ,lineType )
        #cv2.imshow('Original',frame)
        cv2.imshow( 'Mask' ,mask )
        cv2.imshow('frame',frame)
        #cv2.imshow('another image',img1)
        #cv2.imshow('Opening',opening)
        #cv2.imshow('Closing',closing)
        #cv2.imshow( 'img' ,img1 )
        k = cv2.waitKey( 5 ) & 0xFF
        if k == 27:
            cap.release( )
            cv2.destroyAllWindows( )
            #global keep_going
            keep_going = False
            break
    # while ( 1 ):
    #     if cv2.waitKey( 1 ) & 0xFF == ord( "r" ):
    #         cv2.destroyAllWindows( )
    #         cap.release( )
    #         break
while ( keep_going ):
    game( )
