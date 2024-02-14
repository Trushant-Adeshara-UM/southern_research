import sys
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QApplication
from interface import Ui_MainWindow
from pypylon import pylon
import numpy as np

class CameraApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(CameraApp, self).__init__(parent)
        self.setupUi(self)

        self.initCam()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(100)

    def initCam(self):
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()
        self.camera.PixelFormat.SetValue("Mono8")
        self.frame_height = self.camera.Height.GetValue()
        self.frame_width = self.camera.Width.GetValue()
        self.camera.ExposureTime.SetValue(200000)
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    def updateFrame(self):
        grabResult = self.camera.RetrieveResult(629596, pylon.TimeoutHandling_ThrowException)

        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono8
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        if grabResult.GrabSucceeded():
            image = converter.Convert(grabResult)
            img = image.Array

            # Create a QImage from the frame
            qImg = QtGui.QImage(img, self.frame_width, self.frame_height, QtGui.QImage.Format_Grayscale8)
            # Set the QPixmap to the QLabel
            self.imgContainer.setPixmap(QtGui.QPixmap.fromImage(qImg))

    def closeEvent(self, event):
        self.camera.StopGrabbing()
        self.camera.Close()
        super().closeEvent(event)
 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())
