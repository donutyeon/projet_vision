from PIL import Image
import cv2
import numpy as np
BLACK_PIXEL = (0, 0, 0)

def _int_to_bin8(gray):
    """Convert an integer tuple to a binary (string) tuple.
    :param rgb: An integer tuple like (220, 110, 96)
    :return: A string tuple like ("00101010", "11101011", "00010110")
    """
    return f'{gray:08b}'

def _int_to_bin16(YCrCb):
    """Convert an integer tuple to a binary (string) tuple.
    :param rgb: An integer tuple like (220, 110, 96)
    :return: A string tuple like ("00101010", "11101011", "00010110")
    """
    Y,Cr,Cb= YCrCb
    return f'{Y:016b}', f'{Cr:016b}', f'{Cb:016b}'

def _bin_to_int(bgr):
    """Convert a binary (string) tuple to an integer tuple.
    :param rgb: A string tuple like ("00101010", "11101011", "00010110")
    :return: Return an int tuple like (220, 110, 96)
    """
    if(len(bgr) !=3):
        print(len(bgr))
    
    b, g, r= bgr
    return int(b, 2), int(g, 2),int(r,2)

def _merge_bgr(YCrCb, gray):
    """Merge two RGB tuples.
    :param rgb1: An integer tuple like (220, 110, 96)
    :param rgb2: An integer tuple like (280, 95, 105)
    :return: An integer tuple with the two RGB values merged.
    """
    Y, Cr, Cb = _int_to_bin16(YCrCb)
    g = _int_to_bin8(gray)
    bgr = Y,Cr[:8] + g,Cb[:8] + g
    return _bin_to_int(bgr)

def _unmerge_rgb(YCrCb):
    """Unmerge RGB.
    :param rgb: An integer tuple like (220, 110, 96)
    :return: An integer tuple with the two RGB values merged.
    """
    Y,Cr,Cb = _int_to_bin16(YCrCb)
    # Extract the last 8 bits (corresponding to the hidden image)
    # Concatenate 8 zero bits because we are working with 8 bit
    new_bgr = Y,Cr[8:],Cb[8:]
    return _bin_to_int(new_bgr)

def merge(imageA, message):
    """Merge image2 into image1.
    :param image1: First image
    :param image2: Second image
    :return: A new merged image.
    """
    imgA=cv2.imread(imageA,cv2.IMREAD_COLOR)
    imgA=cv2.resize(imgA,(imgA.shape[1]//4,imgA.shape[0]//4))
    imgB=np.full(imgA.shape,255,dtype=np.uint8)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL  
    # org
    org = (0, 20)        
    # fontScale
    fontScale = 1        
    # Blue color in BGR
    color = (0, 0, 0)        
    # Line thickness of 2 px
    thickness = 2
    imgB=cv2.cvtColor(imgB,cv2.COLOR_BGR2GRAY)
    h,w=imgB.shape
    height=25
    width=15
    imgA=cv2.cvtColor(imgA,cv2.COLOR_BGR2YCrCb)
    imgA = np.array(imgA, dtype = np.uint16)
    imgA *= 255
    #imgA=cv2.cvtColor(imgA,cv2.COLOR_BGR2YCrCb)
    msg_len=len(message)
    nb_characters=w//width
    i=0
    while i < msg_len:
        if i+nb_characters > msg_len:
            cv2.putText(imgB, message[i:], org, font,fontScale, color, thickness, cv2.LINE_8)
            #string[i-nb_characters:]
        cv2.putText(imgB, message[i:i+nb_characters], org, font,fontScale, color, thickness, cv2.LINE_8)
        org=(org[0],org[1]+height)
        i+=nb_characters
    cv2.imshow("caca",imgB)
    # Check the images dimensions
    # if imgB.shape[0] > imgA.shape[0] or imgB.shape[1] > imgA.shape[1]:
    #     raise ValueError('Image 2 should be smaller than Image 1!')

    new_image = np.zeros(imgA.shape,dtype=np.uint16)
    # new_map = new_image.load()

    for y in range(h):
        for x in range(w):
            # is_valid = lambda: i < image2.size[0] and j < image2.size[1]
            YCrCb = imgA[y,x]
            #bgr2 = imgB[y, x] #if is_valid() else self.BLACK_PIXEL
            new_image[y, x] = _merge_bgr(YCrCb, imgB[y,x])
    print(new_image[0,0])
    global before
    before=new_image.copy()
    new_image=cv2.cvtColor(new_image,cv2.COLOR_YCrCb2BGR)
    
    return new_image

def unmerge(image):
    """Unmerge an image.
    :param image: The input image.
    :return: The unmerged/extracted image.
    """
    img = cv2.imread(image,-1)
    h,w,c=img.shape
    # Create the new image and load the pixel map
    new_image = np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
    print(img[0,0])
    global after
    after=img.copy()
    diff=np.mean(before[1]-after[1])
    print (diff)
    diffcb=np.mean(before[2]-after[2])
    print(diffcb)
    for y in range(h):
        for x in range(w):
            u=_unmerge_rgb(img[y,x])
            # bi=_int_to_bin16(img[y,x])
            # bin1=bi[1]
            # bin1=bin1[:8]+'00000000'            
            # bin2=bi[2]
            # bin2=bin2[:8]+'00000000'
            # new=(bi[0],bin1,bin2)
            # ent=_bin_to_int(new)
            new_image[y, x] = (u[1]+u[2])//2
    return new_image

message="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
imgA='dog.jpg'
output_image='resultat.png'
merged=merge(imageA=imgA,message=message)
cv2.imwrite(output_image, merged)

unmerged=unmerge('resultat.png')
cv2.imshow('aaaaaaaaaa',unmerged)
cv2.waitKey(0)
cv2.destroyAllWindows()
