import cv2
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)

# Allow the system to sleep for 3 seconds before the webcam initializes
# This is to ensure that the webcam has enough time to start properly
import time
time.sleep(3)

# Capturing background
background = 0
for i in range(30):
    ret, background = cap.read()

# Flip the background so it is not inverted
background = np.flip(background, axis=1)

# Main loop
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Flip the frame so it is not inverted
    frame = np.flip(frame, axis=1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color range for cloak
    lower_red = np.array([100, 40, 40])        
    upper_red = np.array([100, 255, 255]) 

    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])

    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask = mask1 + mask2

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # Replacing the cloak part with background
    frame[np.where(mask == 255)] = background[np.where(mask == 255)]

    cv2.imshow("Invisibility Cloak", frame)
    k = cv2.waitKey(10)
    if k == 27:
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
