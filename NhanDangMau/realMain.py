import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, \
    QDesktopWidget, QGridLayout, QFrame, QTabWidget, QFileDialog,\
    QFileSystemModel, QGraphicsScene
from PyQt5.QtGui  import QPixmap, QImage
# from PyQt5.QtCore.QtObject import 
from ui_mainWindow import Ui_MainWindow
from reader import reader
from detector import detector
from cropper.cropper import crop_card
from detector.detector import detect_info
import cv2 as cv
from vi_symspellpy import fixAddress

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.show()
        self.initialize()
    def initialize(self):
        self.dirModel = QFileSystemModel()
        # ID Card
        self.dirPath = ''
        self.pathImage = ''
        self.warped = None
        self.dirModel.setRootPath(self.dirPath)
        self.treev_CICard.setRootIndex(self.dirModel.index(self.dirPath+"\\"))
        self.btnOpen_CICard.clicked.connect(self.load_image_directory)
        self.btnSelect_CICard.clicked.connect(self.crop_image)
        self.treev_CICard.setModel(self.dirModel)
        self.treev_CICard.setRootIndex(self.dirModel.index(self.dirPath))
        self.treev_CICard.clicked.connect(self.update_image)
        self.btnExtract_CICard.clicked.connect(self.extract_data)
    # Load folder
    def load_image_directory(self):
        fileName = QFileDialog.getExistingDirectory(self, "Open Folder", "", \
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if fileName:
            print(fileName)
        self.dirPath = fileName
        self.dirModel.setRootPath(self.dirPath)
        self.treev_CICard.setRootIndex(self.dirModel.index(self.dirPath+"\\"))
        
    def update_image(self, index):
        self.pathImage = self.dirModel.fileInfo(index).absoluteFilePath()
        grvsize = self.grapvRaw_CICard.size()
        resize_width = grvsize.width()
        resize_height = grvsize.height()
        pixmap = QPixmap(self.pathImage).scaled(resize_width-10, resize_height-10)
        scene = QGraphicsScene()
        scene.addPixmap(pixmap);
        self.grapvRaw_CICard.setScene(scene);
        self.grapvRaw_CICard.show();

    def crop_image(self):
        self.warped = crop_card(self.pathImage)
        if self.warped is None:
            print('Cant find id card in image - Cant crop')
        height, width, channel = self.warped.shape
        bytesPerLine = 3 * width
        pixmap = QPixmap(QImage(self.warped.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())
        # Lay kich thuoc cua container chua anh da crop
        grvsize = self.grapv_CICard.size()
        resize_width = grvsize.width()
        resize_height = grvsize.height()
        # Hien thi anh da crop sau khi resize
        scene = QGraphicsScene()
        scene.addPixmap(pixmap.scaled(resize_width-10, resize_height-10))
        self.grapv_CICard.setScene(scene);
        self.grapv_CICard.show();
    
    def extract_data(self):
        try:
            face, number_img, name_img, dob_img, gender_img, nation_img, \
                country_img, address_img, country_img_list, address_img_list = detect_info(
                    self.warped)
        except:
            print('Cant find id card in image - Cant detect area')
            return
        cv.imwrite('temp.jpg',face)
        # Hien thi anh nho
        pixmap = QPixmap(QImage('temp.jpg'))
        # Lay kich thuoc cua container chua anh da crop
        grvsize = self.grapvFace_CICard.size()
        resize_width = grvsize.width()
        resize_height = grvsize.height()
        # Hien thi anh da crop sau khi resize
        scene = QGraphicsScene()
        scene.addPixmap(pixmap.scaled(resize_width-10, resize_height-10))
        self.grapvFace_CICard.setScene(scene);
        self.grapvFace_CICard.show();

        number_text = reader.get_id_numbers_text(number_img)
        name_text = reader.get_name_text(name_img)
        dob_text = reader.get_dob_text(dob_img)
        gender_text = reader.get_gender_text(gender_img)
        nation_text = reader.get_nation_text(nation_img)
        country_text = reader.process_list_img(country_img_list, is_country=True).replace('\n', ',')
        address_text = reader.process_list_img(address_img_list, is_country=False).replace('\n', ',')
        self.txtbNumber_CICard.document().setPlainText(number_text)
        self.txtbName_CICard.document().setPlainText(name_text)
        self.txtbDOB_CICard.document().setPlainText(dob_text)
        self.txtbSex_CICard.document().setPlainText(gender_text)
        self.txtbNation_CICard.document().setPlainText(nation_text)
        self.txtbHomeTown_CICard.document().setPlainText(country_text)
        self.txtbHome__CICard.document().setPlainText(address_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit( ret )