import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
from PyQt5.QtGui import QPixmap
from mainwindow import *
import os


class MyWindow(QMainWindow, Ui_MainWindow):
    IMAGE_EXT = "jpg"
    def __init__(self, model,file_path,parent=None):
        super(MyWindow, self).__init__(parent)
        self.model=model
        self.file_path=file_path
        self.setupUi(self)
        self.curTrace=None
        self.curTraceFile=None
        self.bind()


    def bind(self):
        self.singleButton.clicked.connect(self.openFile)
        self.detectOnceButton.clicked.connect(self.detectOnce)
        self.multiButton.clicked.connect(self.openDir)
        self.detectMultiButton.clicked.connect(self.detectAll)


    def openDir(self):
        pass

    def openFile(self):
        file=self.chooseFile()

        self.curImageFile=self.getCurImagePath(file)
        self.curTraceFile=file

        self.curTrace = self.getTrace(file)

        self.showTrace()

    def chooseFile(self):
        fileName = QFileDialog.getOpenFileNames(self, '选择状态序列的csv文件', self.file_path, "All Files(*);;Text Files(*.csv)")
        return fileName


    def getTrace(self,file):
        return None


    def getCurImagePath(self,fileName):
        dirName,name=os.path.split(fileName)
        imgName=os.path.splitext(name)[0]+self.IMAGE_EXT
        imgPath=os.path.join(dirName.split(os.path.sep)[:-1],"image",imgName)
        return imgPath

    def showTrace(self):
        pixmap = QPixmap(self.curImageFile)  # 按指定路径找到图片
        self.traceDisplayer.setPixmap(pixmap)  # 在label上显示图片
        self.traceDisplayer.setScaledContents(True)  # 让图片自适应label大小


    def detectAll(self):
        pass

    def detectOnce(self):
        pass




if __name__ == '__main__':
    app = QApplication(sys.argv)
    model=None
    myWin = MyWindow(model,os.path.join(os.getcwd(),"vit_for_action","output","output-200-2nd"))
    myWin.show()
    sys.exit(app.exec_())