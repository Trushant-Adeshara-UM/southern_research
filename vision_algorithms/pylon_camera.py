#################################################
# File: pylon_camera.py                         #
# Class: PylonCamera                            #
#################################################

# Import python module
from pypylon import pylon
import yaml
import cv2

class PylonCamera:
    """
    # ToDo
    """

    def __init__(self, camera_name):
        
        # Load camera_config.yaml file
        with open('./config/camera_config.yaml', 'r') as file:
            self.camera_config = yaml.safe_load(file)

        # Define camera with model
        self.camera_name = camera_name
        self.camera_dev_id = self.camera_config['cameras'][self.camera_name][0]
        self.camera_model = self.camera_config['cameras'][self.camera_name][1]

        # Define camera parameter filename
        self.camera_param_filename = self.camera_name + ".pfs"

        # Define camera parameter filepath
        self.camera_param_filepath = "./config/pfs/" + self.camera_param_filename

        # Instantiate camera
        self.tlFactory = pylon.TlFactory.GetInstance()
        self.devices = self.tlFactory.EnumerateDevices()
        self.camera = pylon.InstantCamera(self.tlFactory.CreateDevice(self.devices[self.camera_dev_id]))

        # Open camera
        self.camera.Open()

        # Set the camera to software trigger mode
        self.camera.TriggerSelector.SetValue("FrameStart")
        self.camera.TriggerMode.SetValue("On")
        self.camera.TriggerSource.SetValue("Software")

        # Fetch camera parameters
        pylon.FeaturePersistence.Load(self.camera_param_filepath, self.camera.GetNodeMap(), True)

        # Start grabbing 
        #self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        self.camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

        while self.camera.IsGrabbing():
            # Execute software trigger
            if self.camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException):
                self.camera.ExecuteSoftwareTrigger() 
    
            # Grab a single frame
            grabResult = self.camera.RetrieveResult(629596, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # Convert the grabbed frame to an OpenCV image
                image = grabResult.Array
                self.image = image.copy()

                # Display the frame
                cv2.imshow('Camera Output', image)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            grabResult.Release()
        
        cv2.destroyAllWindows()
        self.camera.StopGrabbing()
        self.camera.Close()

    def getImage(self):
        return self.image 



if __name__ == '__main__':
    test = PylonCamera('measurement_camera')


