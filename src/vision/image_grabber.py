import cv2
import sys

sys.path.insert(0, 'C:\\Users\\trushant\\southern_research\\src')

from vision.camera_controller import CameraController

class ImageGrabber:
    def __init__(self, camera_controller):
        self.camera_controller = camera_controller
    
    def grab_image(self):
        # Make sure the camera is ready and start grabbing
        if not self.camera_controller.is_grabbing():
            self.camera_controller.start_grabbing()
        
        # Trigger the camera to capture an image
        self.camera_controller.execute_software_trigger()
        
        # Retrieve the captured image
        grab_result = self.camera_controller.retrieve_result()
        if grab_result.GrabSucceeded():
            # Access the image data and process it
            img = grab_result.GetArray()
        else:
            print("Failed to grab image.")
        
        grab_result.Release()
        return img

# Example usage:
if __name__ == "__main__":
    camera_controller = CameraController("measurement_camera")
    camera_controller.configure_for_software_trigger()
    
    image_grabber = ImageGrabber(camera_controller)
    
    try:
        # Grab a single image
        image = image_grabber.grab_image()
        
        cv2.imwrite('test.jpg', image)
            
        cv2.destroyAllWindows()
    finally:
        camera_controller.stop_grabbing()
        camera_controller.close()

