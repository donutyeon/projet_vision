import cv2
import numpy as np
from random import random, randint   # add any other functions you need here



def game( ):
    dx = 4 #values with which the ball's pixel x coord increases
    dy = 4 #values with which the ball's pixel y coord increases
    dx1 =4 
    dy1 =4
    x1 = 90 #initial x coord values for ball's top left corner
    x2 = 100 #initial x coord values for ball's bottom right corner
    y1 = 150 #initial y coord values for ball's top left corner
    y2 = 160 #initial y coord values for ball's bottom right corner
    x3 = 150
    y3 = 150
    x4 = 150
    x5 = 10
    x6 = 60
    y5 = 420
    y6 = 410
    x7 = 10
    y7 = 50
    x8 = 60
    y8 = 60
    f=0
    x11 = []

    for i in range(4):
        x11.append([])
     



        for j in range(18):
            x11[i].append([])
         
            
        for j in range(18):
            x9 = x7 + 60*j
        
            y9 = y7 + 20*i
            
            x11[i][j] = str(x9)+"_"+str(y9)
          
                
    
    
 

    cap = cv2.VideoCapture( 0 )
    while( 1 ):
        _, frame = cap.read( )
        hsv = cv2.cvtColor( frame ,cv2.COLOR_BGR2HSV ) #frame in hsv format
        lower_red = np.array([110,50,50]) #lower hsv range of blue colour
        upper_red = np.array([130,255,255]) #upper hsv range of blue colour
        # lower = np.array( [ 50 ,0 ,0 , ] ) 
        # upper = np.array( [ 35,0 ,0 , ]) #hailla abhi bhi comments padh rahe ho tum banoge asli coderss
        # mask1 = cv2.inRange( hsv ,lower ,upper ) #itna padh hi liyatho khud hi guess marlo
        mask = cv2.inRange( hsv ,lower_red ,upper_red ) #arey last wala guess maro phir yai padhna
        
        res = cv2.bitwise_and( frame, frame, mask= mask )

        kernel = np.ones( ( 5 ,5 ), np.uint8 )
        
        mask = cv2.erode( mask ,kernel ,iterations=1 )
        mask = cv2.dilate( mask,kernel ,iterations=1 )
        #closing = cv2.morphologyEx( mask ,cv2.MORPH_CLOSE ,kernel )
        contours,hierarchy = cv2.findContours( mask ,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE )
        
        for i in range( 0, len(contours) ):
            if ( i % 1 == 0 ):
                cnt = contours[ i ]


                x,y,w,h = cv2.boundingRect( cnt )
                if ( w*h > 2500 ):
                    cv2.drawContours( mask ,contours ,-1, (255,255,0), 3 )
                    
                    img1 = cv2.rectangle( frame,( 640-(x3-25) ,y6 ), ( 640-(x3+25) ,y6+10 ), ( 255 ,255 ,255 ), -1 )
                    cv2.rectangle( mask, ( x ,y ) ,( x+w ,y+h ) ,( 255 ,0 ,0 ) ,2 )
                    x3 = int( ( x + ( w/2 ) ) )
                    y3 = int( ( y + ( h/2 ) ) )
                    
                   
              
         
            
            
            
            
        #agar neeche kya kiya hai samja tho mujai bhi batao plz    
        
        x1 = x1 + dx
        y1 = y1 + dy
        y2 = y2 + dy
        x2 = x2 + dx
        img1 = cv2.rectangle( frame, ( x1 ,y1 ), ( x2 ,y2 ), ( 255 ,255 ,255 ), -1 )
        a = random()
        for i in range(4):
            for j in range(18):
                
                rec = x11[i][j]
                
                    
                if rec != []:
                    rec1 = str(rec)

                    rec_1 = rec1.split("_")
    
                    x12 = int(rec_1[0])
                    y12 = int(rec_1[1])
               
                
                    
                    
                    
                
                
                img1 = cv2.rectangle( frame, ( x12 , y12 ), ( x12+50 , y12+10 ), ( 210 ,90+(10*j) ,110+(20*j) ), -1 )
        if ( x2 >= 640 ):
            dx = -(randint(1, 5))
            
            
        for i in range(4):
            for j in range(18):
                ree = x11[i][j]
                if ree != []:
                    ree1 = str(ree)
                    ree_1 = ree1.split("_")
                    x13 = int (ree_1[0])
                    y13 = int (ree_1[1])
                    if (((x13 <= x2 and x13+50 >=x2) or (x13 <= x1 and x13+50 >=x1)) and y1<=y13 ) or (y1<=50):
                        dy = randint(1,5)
                        x11[i][j]=[]
                        f = f+1
                        break                       
                       
        score = "SCORE : "+str(f)
        font = cv2.FONT_HERSHEY_SIMPLEX
            
        bottomLeftCornerOfText = ( 230 ,25 )
        fontScale              = 1
        fontColor              = ( 210 ,120 ,120 )
        lineType               = 2
        cv2.putText( img1 ,score,bottomLeftCornerOfText ,font ,fontScale ,fontColor ,lineType )
                         
 
        if ( x1 <= 0 ):
            dx = randint(1,5)
        if ( y2 >= y6 ):
            if (640-( x3-25 ) >= x2 and 640-( x3+25 ) <= x2) or (640-( x3-25 ) >= x1 and 640-( x3+25 ) <= x1):
                
                dy = -(randint(1, 5))
        if y2 > y6:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = ( 230 ,25 )
            fontScale              = 1
            fontColor              = ( 255 ,255 ,255 )
            lineType               = 2
            

            cv2.putText( img1 ,'GAME OVER!' ,bottomLeftCornerOfText ,font ,fontScale ,fontColor ,lineType )        
            if y2 > y6+40:
                break
        #cv2.imshow('Original',frame)
        cv2.imshow( 'Mask' ,mask )
        cv2.imshow('frame',frame)
        #cv2.imshow('Opening',opening)
        #cv2.imshow('Closing',closing)
        #cv2.imshow( 'img' ,img1 )
        k = cv2.waitKey( 5 ) & 0xFF
        if k == 27:
            break
    while ( 1 ):
        if cv2.waitKey( 1 ) & 0xFF == ord( "r" ):
            cv2.destroyAllWindows( )
            cap.release( )
            break
while ( 1 ):
    game( )
