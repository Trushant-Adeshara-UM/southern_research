import cv2
import numpy as np

def calculate_image_intensity(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate the average intensity
    average_intensity = np.mean(gray_image)
    
    # Calculate the intensity for each pixel and return the results
    pixel_intensities = gray_image.flatten()
    
    return average_intensity, pixel_intensities

# Replace 'path_to_your_image.jpg' with the path to the image you want to analyze
image_path = './data/vertical_full.png'
average_intensity, pixel_intensities = calculate_image_intensity(image_path)

print(f"Average Intensity: {average_intensity}")
print(f"Pixel Intensities: {pixel_intensities[:100]}") # Prints the first 100 pixel intensities

