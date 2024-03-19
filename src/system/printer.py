# Import python modules
import time
import sys
import cv2

base_path = 'C:\\Users\\trushant\\southern_research\\src'
sys.path.insert(0, base_path)

from stages.stage_control import Aerotech

from vision.camera_controller import CameraController
from vision.image_grabber import ImageGrabber
from vision.line_width_estimator import LineWidthEstimator

class Printer:
    def __init__(self, ref_line_width):
        # Axis specifier
        self.xaxis = 0
        self.yaxis = 1
        self.zaxis = 2

        # Initial speed in each axis
        self.xspeed = 5
        self.xspeed_fast = 50
        self.yspeed = 50
        self.zspeed = 50
        self.zspeed_slow = 0.3

        self.current_x = 0
        self.current_y = 0

        self.pressure = 0

        self.recipe = []
        self.starting_locations = []
        
        self.controller = None

        self.current_pressure = 0
        self.current_location = [0, 0, 0]
        self.base_camera_offset = [-98.39, 1.135, 12] # Offset from needle zero to camera
        self.camera_offset = self.base_camera_offset.copy()
        self.print_location = [0, 0, 0]
        self.moving_height = 10
        self.verbose = 3

        self.ref_width = ref_line_width
        self.estimated_line_width = 0

        # Initialize stages using Aerotech class
        self.staging = Aerotech(material=0, incremental=True) # Use incremental movements
        self.staging.send_message('~INITQUEUE\n') # Initialize the queue
        self.vdisp("Initialized Printer class")

    def vdisp(self, s, l=1):
        if self.verbose >= 1:
            print(f'    P: {s}')

    def get_performance_parameters(self, performance_params):
        return self.controller.get_performance_parameters(length, resistance)

    def get_process_parameters(self, length, resistance):
        return self.controller.get_process_parameters(performance_params)

    def update_gain(self, new_gain):
        self.controller.update_gain(new_gain)

    def save_controller_properties(self, filename):
        self.controller.save_controller(filename)

    def load_controller(self, filename):
        self.controller.load_controller(filename)

    def set_pressure(self, pressure):
        self.vdisp(f'Setting printing pressure to {pressure} PSI')
        voltage = 0.0844 * pressure + 0.0899

        if voltage < 0.1:
            voltage = 0
            self.vdisp("Voltage too low, setting to 0")
            self.staging.setPressure(voltage)
            self.current_pressure = 0
        elif voltage > 2:
            voltage = 2
            self.vdisp("Voltage too high, setting it to 2")
            self.staging.setPressure(voltage)
            self.current_pressure = (voltage - 0.0899) / 0.0844
        else:
            self.staging.setPressure(voltage)
            self.curretn_pressure = pressure

    def linear_print(self, axis, distance, speed):
        #performance_params = self.get_performance_parameters(distance, resistance)
        #process_params = self.get_process_parameters(performance_params)
        self.set_pressure(self.pressure)
        if (axis == 0):
            self.staging.goto(x=distance, f=speed)
        elif (axis == 1):
            self.staging.goto(y=distance, f=speed)
        elif (axis == 2):
            self.staging.goto(z=distance, f=speed)
        else:
            raise Exception("Trying to move via a nonexistent axis")
        self.set_pressure(0)
        self.current_location = [self.staging.x, self.staging.y, self.staging.z]

    def linear(self, axis, distance, speed):
        if (axis == 0):
            self.staging.goto(x=distance, f=speed)
        elif (axis == 1):
            self.staging.goto(y=distance, f=speed)
        elif (axis == 2):
            self.staging.goto(z=distance, f=speed)
        else:
            raise Exception("Trying to move via a nonexistent axis")
        self.current_location = [self.staging.x, self.staging.y, self.staging.z]

    def grab_image(self):
        camera_controller = CameraController("measurement_camera")
        camera_controller.configure_for_software_trigger()

        image_grabber = ImageGrabber(camera_controller)
        image = image_grabber.grab_image()

        camera_controller.stop_grabbing()
        camera_controller.close()

        return image

    def estimate_line_width(self, image):
        estimator = LineWidthEstimator(image)
        contour = estimator.contour_detection()
        points, _, line_image = estimator.line_extraction(contour)
        line_width = estimator.line_width(points, self.ref_width)
        
        return line_width

    def linear_estimator(self, axis, distance, speed):

        intervals = [(4 * distance)/10, (1 * distance)/10, (1 * distance)/10 ]
        line_widths = []

        cnt = 1
        for interval in intervals:

            if (axis == 0):
                self.staging.goto(x=interval, f=speed)
            elif (axis == 1):
                self.staging.goto(y=interval, f=speed)
            elif (axis == 2):
                self.staging.goto(z=interval, f=speed)
            else:
                raise Exception("Trying to move via a nonexistent axis")
            
            captured_img = self.grab_image()
            
            t_str = time.strftime("%Y%m%d-%H%M%S")
            img_str = "itr" + str(cnt) + "-" + t_str + "test" + ".png"

            cv2.imwrite(img_str, captured_img)
            cnt += 1
            line_widths.append(self.estimate_line_width(captured_img))
        
        if len(line_widths) != 0:
            self.estimated_line_width = sum(line_widths) / len(line_widths)
        
        self.current_location = [self.staging.x, self.staging.y, self.staging.z]

        return self.estimated_line_width

    def move_to_location(self, location):
        current_z = self.current_location[2]
        self.linear(self.zaxis, self.moving_height - current_z, self.zspeed)

        current_x = self.current_location[0]
        self.linear(self.xaxis, location[0] - current_x, self.xspeed)

        current_y = self.current_location[1]
        self.linear(self.yaxis, location[1] - current_y, self.yspeed)

        current_z = self.current_location[2]
 
        self.linear(self.zaxis, 2 * (location[2] - current_z) / 3, self.zspeed)
        self.linear(self.zaxis, (location[2] - current_z) / 3, self.zspeed_slow)

    def move_to_camera(self):
        current_z = self.current_location[2]
        self.linear(self.zaxis, self.moving_height - current_z, self.zspeed)

        current_x = self.current_location[0]
        self.linear(self.xaxis, 9 * (self.camera_offset[0] - current_x) / 10, self.xspeed_fast)
        self.linear(self.xaxis, (self.camera_offset[0] - current_x) / 10, self.xspeed)

        current_y = self.current_location[1]
        self.linear(self.yaxis, self.camera_offset[1] - current_y, self.yspeed)

        current_z = self.current_location[2]
        #self.linear(self.zaxis, 2 * (self.camera_offset[2] - current_z) / 3, self.zspeed)
        self.linear(self.zaxis, self.camera_offset[2] - current_z, self.zspeed)

    def move_to_nozzle(self):
        current_z = self.current_location[2]
        self.linear(self.zaxis, self.moving_height - current_z, self.zspeed)

        current_x = self.current_location[0]
        self.linear(self.xaxis, 9 * (self.print_location[0] - current_x) / 10, self.xspeed_fast)
        self.linear(self.xaxis, (self.print_location[0] - current_x) / 10, self.xspeed)

        current_y = self.current_location[1]
        self.linear(self.yaxis, self.print_location[1] - current_y, self.yspeed)

        current_z = self.current_location[2]
        self.linear(self.zaxis, 6 * (self.print_location[2] - current_z) / 7, self.zspeed)
        self.linear(self.zaxis, (self.print_location[2] - current_z ) / 7, self.zspeed_slow)

        for idx, (prt, curr) in enumerate(zip(self.print_location, self.current_location)):
            if abs(prt - curr) > 1:
                raise ValueError("Error between print location and current location greater than 1mm!")
