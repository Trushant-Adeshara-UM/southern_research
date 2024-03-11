# Import python modules
import time
import sys

sys.path.insert(0, 'C:\\Users\\trushant\\southern_research\\src')

from stages.stage_control import Aerotech

class Printer:
    def __init__(self, *args, **kwargs):
        # Axis specifier
        self.xaxis = 0
        self.yaxis = 1
        self.zaxis = 2

        # Initial speed in each axis
        self.xspeed = 0.5
        self.yspeed = 0.5
        self.zspeed = 0.5
        self.zspeed_slow = 0.1

        self.current_x = 0
        self.current_y = 0

        self.recipe = []
        self.starting_locations = []
        
        self.controller = None

        self.current_pressure = 0
        self.current_location = [0, 0, 0]
        self.camera_offset = [99, 3, -7] # Offset from needle zero to camera
        self.print_location = [0, 0, 0]
        self.moving_height = 10
        self.verbose = 3

        # Initialize stages using Aerotech class
        self.staging = Aerotech(material=0, incremental=True) # Use incremental movements
        self.staging.send_message('~INITQUEUE\n') # Initialize the queue
        print(self.staging.x)
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

    def linear_print(self, axis, distance, resistance):
        performance_params = self.get_performance_parameters(distance, resistance)
        process_params = self.get_process_parameters(performance_params)
        pressure = process_params['pressure']
        speed = process_params['speed']
        self.set_pressure(pressure)
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
        self.linear(self.xaxis, self.camera_offset[0] - current_x, self.xspeed)

        current_y = self.current_location[1]
        self.linear(self.yaxis, self.camera_offset[1] - current_y, self.yspeed)

        current_z = self.currernt_location[2]
        self.linear(self.zaxis, 2 * (self.camera_offset[2] - current_z) / 3, self.zpeed)
        self.linear(self.zaxis, (self.camera_offset[2] - current_z) / 3, self.zspeed_slow)

    def move_to_nozzle(self):
        current_z = self.current_location[2]
        self.linear(self.zaxis, self.moving_height - current_z, self.zspeed)

        current_x = self.current_location[0]
        self.linear(self.x_axis, self.print_location[0] - current_x, self.xspeed)

        current_y = self.current_location[1]
        self.linear(self.y_axis, self.print_location[1] - current_y, self.yspeed)

        current_z = self.current_location[2]
        self.linear(self.zaxis, 2 * (self.camera_offset[2] - current_z) / 3, self.zspeed)
        self.linear(self.zaxis, (self.camera_offset[2] - current_z ) / 3, self.zpeed_slow)

        if self.print_location != self.current_location:
            raise ValueError("Something went wrong with moving!")
