# Import pypylon module
from pypylon import pylon

# Generate camera instance
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()

# Access and set camera width
new_width = camera.Width.Value - camera.Width.Inc
if new_width >= camera.Width.Min:
    camera.Width.Value = new_width

# Set number of images to grab
numberOfImagesToGrab = 10
camera.StartGrabbingMax(numberOfImagesToGrab)

# Iterate to capture camera frames
while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data.
        print("SizeX: ", grabResult.Width)
        print("SizeY: ", grabResult.Height)
        img = grabResult.Array
        print("Gray value of first pixel: ", img[0,0])

    grabResult.Release()
camera.Close()
