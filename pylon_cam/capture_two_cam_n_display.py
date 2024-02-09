from pypylon import pylon
import cv2

def set_exposure_camera1(val):
    # Set exposure for camera 1
    camera1.ExposureTime.SetValue(val)

def set_exposure_camera2(val):
    # Set exposure for camera 2
    camera2.ExposureTime.SetValue(val)

# Instantiate and open cameras
tlFactory = pylon.TlFactory.GetInstance()
devices = tlFactory.EnumerateDevices()
if len(devices) < 2:
    raise RuntimeError("Not enough cameras found")

camera1 = pylon.InstantCamera(tlFactory.CreateDevice(devices[0]))
camera2 = pylon.InstantCamera(tlFactory.CreateDevice(devices[1]))

camera1.Open()
camera2.Open()

# Set initial parameters for both cameras (disable auto exposure as an example)
camera1.ExposureAuto.SetValue('Off')
camera2.ExposureAuto.SetValue('Off')

# Start grabbing for both cameras
camera1.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
camera2.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# Create OpenCV windows
cv2.namedWindow('Camera 1 Output', cv2.WINDOW_NORMAL)
cv2.namedWindow('Camera 2 Output', cv2.WINDOW_NORMAL)

# Create exposure sliders for both windows
cv2.createTrackbar('Exposure 1', 'Camera 1 Output', 0, 20000, set_exposure_camera1)
cv2.createTrackbar('Exposure 2', 'Camera 2 Output', 0, 20000, set_exposure_camera2)

while camera1.IsGrabbing() and camera2.IsGrabbing():
    grabResult1 = camera1.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    grabResult2 = camera2.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult1.GrabSucceeded() and grabResult2.GrabSucceeded():
        # Convert grab results to OpenCV format
        image1 = grabResult1.Array
        image2 = grabResult2.Array

        # Show images in their respective windows
        cv2.imshow('Camera 1 Output', image1)
        cv2.imshow('Camera 2 Output', image2)

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release grab results
    grabResult1.Release()
    grabResult2.Release()

# Clean up
cv2.destroyAllWindows()
camera1.StopGrabbing()
camera2.StopGrabbing()
camera1.Close()
camera2.Close()

