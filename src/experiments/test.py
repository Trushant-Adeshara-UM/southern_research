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
    pressure = 20

    test = Printer(ref_line_width)
    test.set_pressure(pressure)
    time.sleep(5)
    test.set_pressure(0)
    
    
        
    
    

    
