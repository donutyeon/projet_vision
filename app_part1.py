import cv2
import numpy as np
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap,QImage
import sys
from PIL import ImageQt
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
                self.decoded=None
                self.show()

        def loadImg(self):
            try:
                self.image=QFileDialog.getOpenFileName(self,"open file ","","png(*.png);;jpeg(*.jpeg);;jpg(*.jpg)")
                self.loaded=cv2.imread(self.image[0],-1)
                self.pic=QPixmap(self.image[0])
                self.pic_label.setScaledContents(True);
                self.pic_label.setPixmap(self.pic)
                self.imageisloaded=True
            except:
                ctypes.windll.user32.MessageBoxW(0, "Wrong path.", "", 0)

        def SaveImg(self):
            try:       
                self.image=QFileDialog.getSaveFileName(self,"save file","","png(*.png);;jpeg(*.jpeg);;jpg(*.jpg)")
                if self.decoded is None:
                    if self.loaded is None:
                        ctypes.windll.user32.MessageBoxW(0, "No picture loaded.", "", 0)
                    else:
                        cv2.imwrite(self.image[0],self.loaded)
                        self.pic=QPixmap(self.image[0])
                        self.pic_label.setScaledContents(True);
                        self.pic_label.setPixmap(self.pic)
                        self.imageisloaded=True

                else:
                    cv2.imwrite(self.image[0],self.decoded)
                    self.pic=QPixmap(self.image[0])
                    self.pic_label.setScaledContents(True);
                    self.pic_label.setPixmap(self.pic)
                    self.imageisloaded=True
            except:
                ctypes.windll.user32.MessageBoxW(0, "No picture loaded.", "", 0)

        def _int_to_bin8(self,gray):
            """
            prend la valeur du bit gris et retourne la valeur binaire sur 8bits
            """
            return f'{gray:08b}'

        def _int_to_bin16(self,YCrCb):
            """
            Prend un tuple (Y,Cr,Cb) et retourne la valeur binaire sur 16bits
            """
            Y,Cr,Cb= YCrCb
            return f'{Y:016b}', f'{Cr:016b}', f'{Cb:016b}'

        def _bin_to_int(self,YCrCb):
            """
            Prend le tuple de chaines de caractères en binaire (Y,Cr,Cb) et retourne les valeurs entières 
            """            
            Y,Cr,Cb= YCrCb
            return int(Y, 2), int(Cr, 2),int(Cb,2)

        def _merge_YCrCb(self,YCrCb, gray):
            """
            Prend le tuple (Y,Cr,Cb) et le bit noir ou blanc, et remplace le 8ème bit de Cb par le bit gray
            """
            Y, Cr, Cb = self._int_to_bin16(YCrCb)
            g = self._int_to_bin8(gray)
            Cb=Cb[:-8]+g[-1]+Cb[-7:-4]+'0111'
            new_YCrCbr = Y,Cr,Cb
            return self._bin_to_int(new_YCrCbr)

        def _unmerge_YCrCb(self,YCrCb):
            """
            Prend le tuple (Y,Cr,Cb) et retourne le 8eme bit de Cb
            """
            Y,Cr,Cb = self._int_to_bin16(YCrCb)
            new_YCrCb = Y,Cr,Cb[-8]
            return self._bin_to_int(new_YCrCb)

        def EncodeListener(self):
            try:

                self.encoded=self.Encode(self.image[0],self.message.toPlainText())
                self.image=QFileDialog.getSaveFileName(self,"save file ","","png(*.png);;jpeg(*.jpeg);;jpg(*.jpg)")
                cv2.imwrite(self.image[0], self.encoded)
                self.pic=QPixmap(self.image[0])
                self.pic_label.setScaledContents(True);
                self.pic_label.setPixmap(self.pic)
            except:
                ctypes.windll.user32.MessageBoxW(0, "No picture loaded.", "", 0)

        def DecodeListener(self):
            try:
                self.Decode(self.image[0])
            except:
                ctypes.windll.user32.MessageBoxW(0, "No picture loaded.", "", 0)

        def Encode(self,imageA, message):
            """
            Génère une image imgB qui contient le message secret , et cache cette image dans l'image imgA
            que l'utilisateur choisit
            """
            imgA=cv2.imread(imageA,cv2.IMREAD_COLOR)
            if (imgA.shape[0]>1300 and imgA.shape[1]>1300):
                imgA=cv2.resize(imgA,(imgA.shape[1]//4,imgA.shape[0]//4))
            imgB=np.full(imgA.shape,255,dtype=np.uint8)
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            org = (0, 20)
            fontScale = 1
            color = (0, 0, 0)
            thickness = 2
            imgB=cv2.cvtColor(imgB,cv2.COLOR_BGR2GRAY)
            h,w=imgB.shape
            height=25
            width=15
            imgA=cv2.cvtColor(imgA,cv2.COLOR_BGR2YCrCb)
            imgA = np.array(imgA, dtype = np.uint16)
            imgA *= 255
            msg_len=len(message)
            nb_characters=w//width
            i=0
            while i < msg_len:
                if i+nb_characters > msg_len:
                    cv2.putText(imgB, message[i:], org, font,fontScale, color, thickness, cv2.LINE_8)
                cv2.putText(imgB, message[i:i+nb_characters], org, font,fontScale, color, thickness, cv2.LINE_8)
                org=(org[0],org[1]+height)
                i+=nb_characters
            imgB[(imgB==255)]=1
            print(np.unique(imgB))

            new_image = np.zeros(imgA.shape,dtype=np.uint16)

            for y in range(h):
                for x in range(w):
                    YCrCb = imgA[y,x]
                    new_image[y, x] = self._merge_YCrCb(YCrCb, imgB[y,x])
                        
            new_image=cv2.cvtColor(new_image,cv2.COLOR_YCrCb2BGR)
            self.loaded=new_image
            return new_image

        def Decode(self,image):
            """
            Prend l'image avec le texte caché et exrait les bits cachés pour générer l'image du texte.
            """
            img = cv2.imread(image,-1)
            h,w,c=img.shape
            new_image = np.zeros((img.shape[0],img.shape[1]),dtype=np.uint8)
            img=cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
            print(img[0,0])
            for y in range(h):
                for x in range(w):
                    new_image[y, x] = self._unmerge_YCrCb(img[y,x])[2]
            new_image[(new_image==1)]=255
            image = QtGui.QImage(new_image, new_image.shape[1],new_image.shape[0],QImage.Format_Grayscale8)
            self.pic=QPixmap(image)
            self.pic_label.setPixmap(self.pic)
            self.imageisloaded=True
            self.loaded=new_image
            return new_image

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()