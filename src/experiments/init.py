# Import python module
import time
import sys
import pdb

sys.path.insert(0, 'C:\\Users\\trushant\\southern_research\\src')

from system.printer import Printer
from control.controller import Controller

if __name__ == '__main__': 
    line_length = 10
    pressure = 20
    ref_line_width = 280

    test = Printer(ref_line_width)
    test.pressure = pressure
     
    print_speed = 0.3

    #test.linear(2, 10, 0.5)
    #test.set_pressure(20)
    #time.sleep(0.75)
    #test.set_pressure(0)

    #update_print_location = [ [0, 13, 0], [0, 26, 0],
    #                          [-2, 0, 0], [-2, 13, 0], [-2, 26, 0],
    #                          [-4, 0, 0], [-4, 13, 0], [-4, 26, 0] ]

    #update_print_location = [ [0, 13, 0], [0, 26, 0], [0, 39, 0], [0, 52, 0], [0, 65, 0] ]
    update_print_location = [ [0, 0, 0] ]

 
    for location in update_print_location:
        #test.linear_print(1, line_length, abs(print_speed))
        test.linear_print(0, -line_length, print_speed)
        test.print_location = location
        test.move_to_nozzle()

        
    
    

    
