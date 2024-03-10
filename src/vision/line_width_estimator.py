# Import python modules
import cv2
import numpy as np
from scipy.signal import medfilt2d

from pylon_camera import PylonCamera

class LineWidthEstimator():
    """
    TODO
    """
    def __init__(self, image):
        self.px_mm_factor = 1.59
        self.threshold_1 = 0.3
        self.threshold_2 = 0.6
        self.threshold_3 = 0.9

        self.image = image

        _, self.binary_threshold_1 = cv2.threshold(self.image, self.threshold_1 * 255, 255, cv2.THRESH_BINARY)
        _, self.binary_threshold_2 = cv2.threshold(self.binary_threshold_1, self.threshold_2 * 255, 255, cv2.THRESH_BINARY)
        _, self.binary_threshold_3 = cv2.threshold(self.binary_threshold_2, self.threshold_3 * 255, 255, cv2.THRESH_BINARY)

        self.binary = self.binary_threshold_3.copy()

        self.contours, _ = cv2.findContours(self.binary.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        self.contour_image = np.zeros((self.binary.shape[0], self.binary.shape[1], 3), dtype=np.uint8)

        for itr, contour in enumerate(self.contours):
            color = [255, 255, 255]
            if len(contour) > 50:
                cv2.drawContours(self.contour_image, self.contours, itr, color, 1)

        self.gray = cv2.cvtColor(self.contour_image, cv2.COLOR_BGR2GRAY)
    
        self.col_pts = np.linspace(0, self.gray.shape[1]-1, 25, dtype=np.uint)
        points = {}
        for col in self.col_pts:
            lister = []
            for row in range(0, self.gray.shape[0]):
                if (self.gray[row][col] > 220):
                    lister.append(row)
            points[col] = lister

        for col, val  in points.items():
            for row in val:
                coord = (col, row)
                cv2.circle(self.contour_image, coord, 5, (255, 255, 255), -1)

        for col, val in points.items():
            cv2.line(self.contour_image, (col, val[0]), (col, val[1]), (255, 255, 255), 3)

        print(points)


def show(image):
    while True:
        cv2.imshow('Output', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()



if __name__ == '__main__':
    cam = PylonCamera('measurement_camera')
    test = LineWidthEstimator(cam.getImage())




