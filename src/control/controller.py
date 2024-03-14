# Import python modules
import numpy as np
from sympy import symbols, diff

class Controller:
    def __init__(self):
        # Properties
        #self.performanceGain = 78927
        #self.performanceBias = 1.8169

        self.processGain = 201.22
        self.processBias = 22.705

        self.processSpeed = 0
        self.LearningRate = 0.2
        self.C = 1

        self.verbose = 3  # Debugging
 

    def derivative_process_speed(self, line_width):
        # Define the symbols
        line_width_sym, processGain_sym, processBias_sym = symbols('line_width processGain processBias')

        # Define the equation
        equation = (processGain_sym / (line_width_sym + processBias_sym))**2

        # Compute the derivative with respect to line_width
        derivative = diff(equation, line_width_sym)

        # Substitute the actual values
        derivative_evaluated = derivative.subs({
            line_width_sym: line_width,
            processGain_sym: self.processGain,
            processBias_sym: self.processBias
        })

        return derivative_evaluated

    def process_model(self, line_width):
        self.processSpeed = (self.processGain / (line_width + self.processBias)) ** 2
        derivative = self.derivative_process_speed(line_width)
        width_error = self.ref_line_width = line_width
        learning_filter = self.C * derivative
        self.processSpeed = self.processSpeed + (learning_filter * width_error)

        return self.processSpeed, width_error


    def save_controller(self, filename):
        controllerData = {
            'Gain': self.Gain, 
            'LearningRate': self.LearningRate, 
            # TODO: Add other relevant properties to save
        }
        # TODO: Implement file saving using Python's file handling methods
        self.vdisp(f"Saved controller to {filename}")

    def load_controller(self, filename):
        self.vdisp(f"Loaded controller from {filename}")
        # TODO: Implement file loading using Python's file handling methods
        # After loading, update the object's properties with the loaded values
        # If the file format is invalid, raise an appropriate error

    def vdisp(self, s, l=1):
        if self.verbose >= l:
            print(f'    C: {s}')

if __name__ == '__main__':
    test = Controller()
    speed, error = test.process_model(280)
    print(abs(speed))

