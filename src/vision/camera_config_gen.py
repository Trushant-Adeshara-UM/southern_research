##################################################
# File: camera_config_gen.py                     # 
# Class: CameraConfigurator                      #
##################################################

# Note:
# No matter in which sequence the cameras are plugged-in,
# they will be attached in ascending order of their name. 

# Import python modules
from pypylon import pylon
import yaml

# ToDo
# Disintegrate all functions from the __init__ method based on their implementation.

class CameraConfigurator:
    """
    # ToDo Complete this
    """
    def __init__(self):
        # CameraConfigurator Class start point.
        print("CameraConfigurator")

        # Maximum number of cameras allowed. (Modify this if more cameras are needed)
        self.maxCameraToUse = 2

        # Get the transport layer factory.
        self.tlFactory = pylon.TlFactory.GetInstance()

        # Get all attached devices and exit application if no devices is found.
        self.devices = self.tlFactory.EnumerateDevices()
        
        if len(self.devices) == 0:
            raise pylon.RuntimeException("No camera present.")

        # Create an array of instant cameras for the found devices and avoid exceeding maxCamerasToUse.
        self.cameras = pylon.InstantCameraArray(min(len(self.devices), self.maxCameraToUse))
       
        # Fetch the number of cameras attached.
        numCamerasFound = self.cameras.GetSize()

         
        # Create and attach all Pylon Devices.
        cam_dict = {}
        for itr, cam in enumerate(self.cameras):
            cam.Attach(self.tlFactory.CreateDevice(self.devices[itr]))
            # Print the model name of the camera.
            print("Using device", cam.GetDeviceInfo().GetModelName())
            cam_dict[itr+1] = [itr, cam.GetDeviceInfo().GetModelName()]

        # Create YAML file data structure
        data = {
                'max_camera': 2,
                'cameras': {
                    'measurement_camera': cam_dict[1], 
                    'nozzle_camera': cam_dict[2],
                    }
                }
        
        # Convert YAML data to string
        yaml_data_str = yaml.dump(data, default_flow_style=False)

        # Add comments to the YAML file
        comments = "##################################################\n" \
                   "# File: camera_config.yaml                       #\n" \
                   "##################################################\n\n" 

        # Combine comments and YAML data
        comment_plus_yaml_str = comments + yaml_data_str

        # ToDo
        # Insert  inline comments if needed
        # comment_plus_yaml_str = comment_plus_yaml_str.replace(" intial value ", "new value with coment")

        # Specify the filename to store YAML data to.
        filename = './config/camera_config.yaml'

        # Writing to a YAML file.
        with open(filename, 'w') as file:
            file.write(comment_plus_yaml_str)

        

if __name__ == "__main__":
    cameras_info = CameraConfigurator()
