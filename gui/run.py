import sys
from PySide2 import QtWidgets
from interface import Ui_MainWindow  # Import the generated class

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)  # Setup the UI from the generated Python code

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyWindow()
    mainWindow.show()
    sys.exit(app.exec_())

