# Import pypylon and opencv modules
from pypylon import pylon
import cv2

def set_exposure(val):
    # Set camera exposure time. The slider value is in microseconds.
    # Please adjust the range according to your camera's capabilities.
    camera.ExposureTime.SetValue(val)

# Create a camera object. This automatically selects the first camera found.
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Open the camera to access parameters.
camera.Open()

# Assuming your camera has manual exposure control, disable auto exposure.
# This might differ based on your camera model.
# Check your camera's user manual for correct parameter names.
camera.ExposureAuto.SetValue('Off') # Might be 'ExposureAuto' or similar.

# Start the camera.
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# Create a window to display the images.
cv2.namedWindow('Camera Output', cv2.WINDOW_NORMAL)

# Create an exposure slider.
# Adjust the maximum value according to your camera's capabilities.
cv2.createTrackbar('Exposure', 'Camera Output', 60, 1000000, set_exposure)

while camera.IsGrabbing():
    # Grab a single frame.
    grabResult = camera.RetrieveResult(629596, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Convert the grabbed frame to an OpenCV image (BGR format).
        image = grabResult.Array
        # Display the frame.
        cv2.imshow('Camera Output', image)

        # Break the loop if 'q' is pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    grabResult.Release()

# Release resources.
cv2.destroyAllWindows()
camera.StopGrabbing()
camera.Close()

