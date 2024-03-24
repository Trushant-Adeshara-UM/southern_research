# Import python module
import time
import sys
import pdb

sys.path.insert(0, 'C:\\Users\\trushant\\southern_research\\src')

from system.printer import Printer
from control.controller import Controller


def write_file_(cnt, ref_line_width, print_speed):
    data1 = str(cnt) + " Reference Line Width: " + str(ref_line_width)
    data2 = str(cnt) + " Print Speed: " + str(print_speed)
    data_arr = [data1, data2]

    with open('run_det.txt', 'a') as file:
        for item in data_arr:
            file.write(f"{item}\n")

def write_file(cnt, ref_line_width, print_speed, width_error, updated_line_width):
    data1 = str(cnt) + " Reference Line Width: " + str(ref_line_width)
    data2 = str(cnt) + " Line Width: " + str(updated_line_width)
    data3 = str(cnt) + " Width Error: " + str(width_error)
    data4 = str(cnt) + " Print Speed: " + str(print_speed)
    
    
    data_arr = [data1, data2, data3, data4]

    with open('run_det.txt', 'a') as file:
        for item in data_arr:
            file.write(f"\n")
            file.write(f"{item}\n")

if __name__ == '__main__':
    
    cnt = 0
    line_length = 15
    ref_line_width = 280
    delta = 10
    pressure = 12

    test = Printer(ref_line_width)
    test.pressure = pressure
    
    ctrl = Controller()
    ctrl.ref_line_width = ref_line_width
 
    
    update_print_location = [ [ 0, 0, 0], [0, 18, 0], [0, 36, 0], [0, 54, 0],
                              [ -1, 0, 0] ]

    print_speed = 0.44

    for location in update_print_location:
        cnt += 1
        test.linear_print(1, line_length, abs(print_speed))
        test.camera_offset[1] = update_print_location[cnt][1] - test.base_camera_offset[1]
        test.move_to_camera()
        updated_line_width = test.linear_estimator(1, -line_length, 50)
        test.print_location = update_print_location[cnt]
        test.move_to_nozzle()
        width_error = ref_line_width - updated_line_width
        write_file(cnt, ref_line_width, print_speed, width_error, updated_line_width)
        prev_speed = print_speed
        test.set_pressure(pressure)
        time.sleep(0.5)

    test.set_pressure(0)



    