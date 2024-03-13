# Import python module
import time
import sys

sys.path.insert(0, 'C:\\Users\\trushant\\southern_research\\src')

from system.printer import Printer

if __name__ == '__main__':
    test = Printer()
    #test.linear(2, 10, 0.5)
    #test.set_pressure(20)
    #time.sleep(0.75)
    #test.set_pressure(0)
    test.move_to_camera()
    test.move_to_nozzle()
    
    

    
