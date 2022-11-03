from PIL import Image
import cv2
import numpy as np
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap,QImage
import sys
import ctypes
BLACK_PIXEL = (0, 0, 0)

class Ui(QtWidgets.QMainWindow):
        def __init__(self):
                super(Ui, self).__init__()
                self.setWindowIcon(QtGui.QIcon('logo_vision.png'))
                self.setIconSize(QtCore.QSize(200,180))
                self.setWindowTitle("Projet Vision")
                uic.loadUi('main_part1.ui', self)
                
                self.upload_button=self.findChild(QtWidgets.QPushButton,'upload_button')
                self.upload_button.clicked.connect(self.loadImg)
                self.save_button=self.findChild(QtWidgets.QPushButton,'save_button')
                self.save_button.clicked.connect(self.SaveImg)
                self.encode_button=self.findChild(QtWidgets.QPushButton,'encode_button')
                self.encode_button.clicked.connect(self.EncodeListener)
                self.decode_button=self.findChild(QtWidgets.QPushButton,'decode_button')
                self.decode_button.clicked.connect(self.DecodeListener)
                self.message=self.findChild(QtWidgets.QPlainTextEdit,'secret_message')
                self.pic_label=self.findChild(QtWidgets.QLabel,'picturelabel')
                self.image=QPixmap('vision.png')
                self.pic_label.setPixmap(self.image)
                self.imageisloaded=True
                self.show()

        def loadImg(self):
            self.image=QFileDialog.getOpenFileName(self,"open file "," ","png(*.png);;jpeg(*.jpeg);;jpg(*.jpg)")
            self.pic=QPixmap(self.image[0])
            self.pic_label.setScaledContents(True);
            self.pic_label.setPixmap(self.pic)
            self.imageisloaded=True
            # self.image=self.convertQImageToMat(self.image)
            # self.imgsrc=self.image
        def SaveImg(self):
            file=QFileDialog.getSaveFileName(self,"open file "," ","png(*.png);;jpeg(*.jpeg);;jpg(*.jpg)")
            self.pic=QPixmap(file[0])
            self.pic_label.setScaledContents(True);
            self.pic_label.setPixmap(self.pic)
            self.imageisloaded=True

        def _int_to_bin8(self,gray):
            """Convert an integer tuple to a binary (string) tuple.
            :param rgb: An integer tuple like (220, 110, 96)
            :return: A string tuple like ("00101010", "11101011", "00010110")
            """
            return f'{gray:08b}'

        def _int_to_bin16(self,YCrCb):
            """Convert an integer tuple to a binary (string) tuple.
            :param rgb: An integer tuple like (220, 110, 96)
            :return: A string tuple like ("00101010", "11101011", "00010110")
            """
            Y,Cr,Cb= YCrCb
            return f'{Y:016b}', f'{Cr:016b}', f'{Cb:016b}'

        def _bin_to_int(self,bgr):
            """Convert a binary (string) tuple to an integer tuple.
            :param rgb: A string tuple like ("00101010", "11101011", "00010110")
            :return: Return an int tuple like (220, 110, 96)
            """
            if(len(bgr) !=3):
                print(len(bgr))
            
            b, g, r= bgr
            return int(b, 2), int(g, 2),int(r,2)

        def _merge_bgr(self,YCrCb, gray):
            """Merge two RGB tuples.
            :param rgb1: An integer tuple like (220, 110, 96)
            :param rgb2: An integer tuple like (280, 95, 105)
            :return: An integer tuple with the two RGB values merged.
            """
            Y, Cr, Cb = self._int_to_bin16(YCrCb)
            g = self._int_to_bin8(gray)
            Cb=Cb[:8]+g[-1]+Cb[9:-4]+'0111'
            bgr = Y,Cr,Cb
            return self._bin_to_int(bgr)

        def _unmerge_rgb(self,YCrCb):
            """Unmerge RGB.
            :param rgb: An integer tuple like (220, 110, 96)
            :return: An integer tuple with the two RGB values merged.
            """
            Y,Cr,Cb = self._int_to_bin16(YCrCb)
            # Extract the last 8 bits (corresponding to the hidden image)
            # Concatenate 8 zero bits because we are working with 8 bit
            new_bgr = Y,Cr,Cb[8]
            return self._bin_to_int(new_bgr)

        def EncodeListener(self):
            self.encoded=self.Encode(self.image[0],self.message.toPlainText())
            self.image=QFileDialog.getSaveFileName(self,"save file "," ","png(*.png);;jpeg(*.jpeg);;jpg(*.jpg)")
            cv2.imwrite(self.image[0], self.encoded)
            self.pic=QPixmap(self.image[0])
            self.pic_label.setScaledContents(True);
            self.pic_label.setPixmap(self.pic)

        def DecodeListener(self):
            self.Decode(self.image[0])

        def Encode(self,imageA, message):
            """Merge image2 into image1.
            :param image1: First image
            :param image2: Second image
            :return: A new merged image.
            """
            imgA=cv2.imread(imageA,cv2.IMREAD_COLOR)
            if (imgA.shape[0]>1300 and imgA.shape[1]>1300):
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
            #cv2.imshow("caca",imgB)
            print(np.unique(imgB))
            imgB[(imgB==255)]=1
            print(np.unique(imgB))

            new_image = np.zeros(imgA.shape,dtype=np.uint16)
            # new_map = new_image.load()

            for y in range(h):
                for x in range(w):
                    # is_valid = lambda: i < image2.size[0] and j < image2.size[1]
                    YCrCb = imgA[y,x]
                    #bgr2 = imgB[y, x] #if is_valid() else self.BLACK_PIXEL
                    new_image[y, x] = self._merge_bgr(YCrCb, imgB[y,x])
                        
            new_image=cv2.cvtColor(new_image,cv2.COLOR_YCrCb2BGR)
            
            return new_image

        def Decode(self,image):
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
            for y in range(h):
                for x in range(w):
                    new_image[y, x] = self._unmerge_rgb(img[y,x])[2]
            new_image[(new_image==1)]=255
            image = QtGui.QImage(new_image, new_image.shape[1],new_image.shape[0],QImage.Format_Grayscale8)
            self.pic=QPixmap(image)
            self.pic_label.setPixmap(self.pic)
            return new_image

# message="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
# imgA='pollo.jpg'
# output_image='resultat.png'
# merged=merge(imageA=imgA,message=message)
# cv2.imwrite(output_image, merged)

# unmerged=unmerge('resultat.png')
# cv2.imshow('aaaaaaaaaa',unmerged)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()