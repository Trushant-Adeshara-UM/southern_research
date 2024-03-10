import time
from Staging import Aerotech

staging = Aerotech(material=0, incremental=True)
staging.send_message('~INITQUEUE\n')
verbose = 3

def vdisp(s, l=1):
    if verbose >= 1:
        print(f'    P: {s}')

def set_pressure(pressure):
    vdisp(f'Setting printing pressure to {pressure} PSI')
    conversion_map = {0.1: 1, 0.2: 2}
    voltage = 0.0844*pressure + 0.0899
    if voltage < 0.1:
        voltage = 0
        vdisp("Voltage too low, setting  to 0")
        staging.setPressure(voltage)
        current_pressure = 0
    elif voltage > 2:
        vdisp("Voltage too high, settign it to 2")
        voltage = 2
        staging.setPressure(voltage)
        current_pressure = (voltage - 0.0899) / 0.0844
    else:
        staging.setPressure(voltage)
        current_pressure = pressure

vdisp("Initialized Printer class")
pressure = 0 
voltage = 0.0844*pressure + 0.0899
print(pressure)
print(voltage)
set_pressure(pressure)
