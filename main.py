import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from Ui_scanner import Ui_MainWindow
from ocr.demo import scanocr

class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.select.clicked.connect(self.load)
        self.dst.clicked.connect(self.setdst)
        self.cancel.clicked.connect(self.close)
        self.scan.clicked.connect(self.startscan)
        self.img_path.setText("please select the folder with images to scan")
        self.dst_path.setText("please select the folder to save your file")
        self.isocr = ''
        
        
        self.path = None
    
    def load(self):
        self.path = QFileDialog.getExistingDirectory(None,"选取文件夹","C:/")
        self.img_path.setText(self.path)
    def setdst(self):
        self.dst = QFileDialog.getExistingDirectory(None,"选取文件夹","C:/")
        self.dst_path.setText(self.dst)
    def startscan(self):
        if self.pdf.isChecked():
            self.model = '1'
        else:
            self.model = ''
        if self.ocr.isChecked():
            self.isocr = '1'
            self.model = '1'
        else:
            self.ocr = ''
        scanocr(self.path,self.dst,self.model,self.isocr)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec())