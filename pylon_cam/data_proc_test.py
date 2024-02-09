# Import pylon data processing module
from pypylon import pylondataprocessing
import os

# Define result storing variable
resultCollector = pylondataprocessing.GenericOutputObserver()

# Create recipe for data processing
recipe = pylondataprocessing.Recipe()
recipe.Load('dataprocessing_barcode.precipe')
recipe.RegisterAllOutputsObserver(resultCollector, pylon.RegistrationMode_Append);
recipe.Start()

for i in range(0, 10):
    if resultCollector.GetWaitObject().Wait(5000):
        result = resultCollector.RetrieveResult()
        variant = result["Barcodes"]
        if not variant.HasError():
            for barcodeIndex in range(0, variant.NumArrayValues):
                print(variant.GetArrayValues(barcodeIndex).ToString())
        else:
            print("Error: " + variant.GetErrorDescription())
    else:
        print("Result timeout")
        break

recipe.Unload()
