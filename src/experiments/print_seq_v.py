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
    delta = 20
    pressure = 20

    test = Printer(ref_line_width)
    test.pressure = pressure
    
    ctrl = Controller()
    ctrl.ref_line_width = ref_line_width

    
    base_speed = ctrl.base_process(ref_line_width)


    write_file_(cnt, ref_line_width, base_speed) 
 
    
    update_print_location = [ [ 0, 0, 0],
                              [ -1.5, 0, 0],
                              [ -2.5, 0, 0], 
                              [ -3.5, 0, 0],
                              [ -4.5, 0, 0],
                              [ -5.5, 0, 0],
                              [ -6.5, 0, 0],
                              [ -7.5, 0, 0], 
                              [ -8.5, 0, 0],
                              [ -9.5, 0, 0],
                              [ -10.5, 0, 0],
                              [ -11.5, 0, 0],
                              [ -12.5, 0, 0] ]

    prev_speed = base_speed

    for location in update_print_location:
        time.sleep(10)
        test.linear_print(1, line_length, abs(prev_speed))
        test.camera_offset[1] = line_length + test.base_camera_offset[1]
        test.camera_offset[0] = update_print_location[cnt][0] + test.base_camera_offset[0]
        test.move_to_camera()
        updated_line_width = test.linear_estimator(1, -line_length, 50)
        test.print_location = update_print_location[cnt+1]
        test.move_to_nozzle()
        print_speed, width_error = ctrl.process_model(updated_line_width, prev_speed)
        write_file(cnt, ref_line_width, print_speed, width_error, updated_line_width)
        prev_speed = print_speed
        cnt+=1

        if abs(width_error) < delta:
            test.set_pressure(0)
            break


    
