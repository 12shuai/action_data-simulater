import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainwindow import *


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, model,parent=None):
        super(MyWindow, self).__init__(parent)
        self.model=model
        self.setupUi(self)
        self.curTrace=None
        self.bind()


    def bin(self):
        self.singleButton.clicked.connect(self.openFile)
        self.detectButton.clicked.connect(self.detectOnce)
        self.multiButton.clicked.connect(self.detectAll)


    def detectOnce(self):
        pass

    def openFile(self):
        file=self.chooseFile()
        trace=self.getTrace(file)
        self.curTrace=trace
        self.show_trace(trace)

    def detectAll(self):
        dir=self.chooseDir()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())