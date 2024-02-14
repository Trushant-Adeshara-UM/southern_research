# Import pylon and qt modules
import sys
import cv2
from pypylon import pylon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer

class PylonStream(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.capture = self.initCam()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(100)  # Update interval in milliseconds

    def initCam(self):
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()
        self.camera.PixelFormat.SetValue("Mono8")
        self.frame_height = self.camera.Height.GetValue()
        self.frame_width = self.camera.Width.GetValue()
        self.camera.ExposureTime.SetValue(200000)
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)


    def initUI(self):
        self.layout = QVBoxLayout()
        self.imageLabel = QLabel(self)
        self.layout.addWidget(self.imageLabel)
        self.setLayout(self.layout)

    def updateFrame(self):
        grabResult = self.camera.RetrieveResult(629596, pylon.TimeoutHandling_ThrowException)

        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono8
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        if grabResult.GrabSucceeded():
            image = converter.Convert(grabResult)
            img = image.Array 
        
            # Create a QImage from the frame
            qImg = QImage(img, self.frame_width, self.frame_height, QImage.Format_Grayscale8)
            # Set the QPixmap to the QLabel
            self.imageLabel.setPixmap(QPixmap.fromImage(qImg))

    def closeEvent(self, event):
        super().closeEvent(event)
        self.capture.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PylonStream()
    ex.resize(640, 480)
    ex.show()
    sys.exit(app.exec_())

