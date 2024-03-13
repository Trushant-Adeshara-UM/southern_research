from pypylon import pylon
import yaml

class CameraController:
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

        self.camera.Open()
    
    def configure_for_software_trigger(self):
        self.camera.TriggerSelector.SetValue("FrameStart")
        self.camera.TriggerMode.SetValue("On")
        self.camera.TriggerSource.SetValue("Software")
    
    def start_grabbing(self):
        self.camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
    
    def stop_grabbing(self):
        self.camera.StopGrabbing()
    
    def close(self):
        self.camera.Close()

    def is_grabbing(self):
        return self.camera.IsGrabbing()

    def execute_software_trigger(self):
        if self.camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException):
            self.camera.ExecuteSoftwareTrigger()
    
    def retrieve_result(self, timeout=5000):
        return self.camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)

