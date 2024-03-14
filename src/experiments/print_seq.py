# Import python module
import time
import sys
import pdb

sys.path.insert(0, 'C:\\Users\\trushant\\southern_research\\src')

from system.printer import Printer
from control.controller import Controller

if __name__ == '__main__':
    
    line_length = 10
    ref_line_width = 280
    delta = 0.1 * ref_line_width

    test = Printer(ref_line_width)
    
    ctrl = Controller()
    
    print_speed, width_error = ctrl.process_model(ref_line_width)

    #test.linear(2, 10, 0.5)
    #test.set_pressure(20)
    #time.sleep(0.75)
    #test.set_pressure(0)

    update_print_location = [ [0, 13, 0], [0, 26, 0],
                              [-2, 0, 0], [-2, 13, 0], [-2, 26, 0],
                              [-4, 0, 0], [-4, 13, 0], [-4, 26, 0] ]

    #update_print_location = [ [0, 13, 0] ]

 
    line_length = 10

    for location in update_print_location:
       
        #if width_error < delta:
        #    break
        print_speed = 0.8
        test.linear(1, line_length, abs(print_speed))
        test.camera_offset[1] = location[1] - test.base_camera_offset[1]
        test.move_to_camera()
        updated_line_width = test.linear_estimator(1, -line_length, 0.7)
        test.print_location = location
        test.move_to_nozzle()
        print_speed, width_error = ctrl.process_model(updated_line_width)
        print("######################################")
        print(f'print speed: {print_speed}')
        print(f'width error: {width_error}')
        
    
    

    
