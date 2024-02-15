import cv2
import numpy as np

img_path = "./data/vertical_full.png"
gray_img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# Apply thresholding to get a binary image
_, binary_img = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Find edges using the Canny edge detector
edges = cv2.Canny(binary_img, 50, 150)
edges_contours = edges

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours 
cv2.drawContours(edges_contours, contours, -1, (0, 255, 0), 2)

cv2.imshow('Origianl Image', gray_img)
cv2.imshow('Binary Image', binary_img)
cv2.imshow('Edges', edges)
cv2.imshow('Contours', edge_contours)
cv2.waitKey(0)
cv2.destroyAllWindows()
