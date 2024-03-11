# Import python modules
import time
import sys

sys.path.insert(0, 'C:\\Users\\trushant\\southern_research\\src')

from stages.stage_control import Aerotech

if __name__ == '__main__':
    # Setting stages to incremental mode
    stages = Aerotech(0, True)

    # Initializing command queue
    stages.send_message('~INITQUEUE\n')

    # Homing axis
    stages.send_message('HOME Z\n')
    stages.send_message('HOME X Y\n')

    # Finding zero position
    # stages.goto(z=-100, f=10)
    # stages.goto(z=-50, f=5)

    # stages.goto(x=130, f=5)
    # stages.goto(x=6.5, f=1)

    # stages.goto(y=-90, f=5)
    # stages.goto(y=-4, f=1)

    # stages.goto(z=-30, f=5)
    # stages.goto(z=-20, f=1.5)
