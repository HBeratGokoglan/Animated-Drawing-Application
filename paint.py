# **** LIBRARY SETUPS ****
# To install necessary libraries, run the following commands:
# pip install mediapipe
# pip install opencv-python

import mediapipe as mp
import cv2
import numpy as np
import time

# Constants for the drawing application
ml = 150  # Margin left for the tool selection area
max_x, max_y = 250 + ml, 50  # Maximum coordinates for the tool selection area
curr_tool = "Select Tool"  # Initially selected tool
time_init = True  # Flag to check if time has been initialized
rad = 40  # Radius for the tool selection indicator
var_inits = False  # Flag to check if the tool drawing variables have been initialized
thick = 2  # Thickness of the lines/shapes drawn
prevx, prevy = 0, 0  # Previous coordinates for drawing

# Function to get the selected tool based on x-coordinate
def getTool(x):
    if x < 50 + ml:
        return "Straight Line"
    elif x < 100 + ml:
        return "Square"
    elif x < 150 + ml:
        return "Draw"
    elif x < 200 + ml:
        return "Circle"
    else:
        return "Eraser"

# Function to check if the index finger is raised
def index_raised(yi, y9):
    if (y9 - yi) > 40:  # If the difference between landmarks indicates the finger is raised
        return True
    return False

# Initialize MediaPipe Hands module
hands = mp.solutions.hands
hand_landmark = hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=1)
draw = mp.solutions.drawing_utils  # Utility for drawing landmarks

# Load drawing tools image
tools = cv2.imread("tools.png")
tools = tools.astype('uint8')  # Ensure the image is in the correct format

# Create a mask for the drawing area
mask = np.ones((480, 640)) * 255  # White mask
mask = mask.astype('uint8')  # Ensure the mask is in the correct format

# Start video capture from the webcam
cap = cv2.VideoCapture(0)

# Main loop for the drawing application
while True:
    _, frm = cap.read()  # Capture a frame from the webcam
    frm = cv2.flip(frm, 1)  # Flip the frame horizontally for a mirror effect

    rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)  # Convert frame to RGB format
    op = hand_landmark.process(rgb)  # Process the frame for hand landmarks

    if op.multi_hand_landmarks:  # If hand landmarks are detected
        for i in op.multi_hand_landmarks:  # Iterate through detected hands
            draw.draw_landmarks(frm, i, hands.HAND_CONNECTIONS)  # Draw hand landmarks on the frame
            x, y = int(i.landmark[8].x * 640), int(i.landmark[8].y * 480)  # Get coordinates of the index finger tip

            # Check if the coordinates are within the tool selection area
            if x < max_x and y < max_y and x > ml:
                if time_init:
                    ctime = time.time()  # Record the current time
                    time_init = False  # Set the flag to false to prevent re-initializing time
                ptime = time.time()  # Get the current time

                # Draw a circle to indicate tool selection
                cv2.circle(frm, (x, y), rad, (0, 255, 255), 1)
                rad -= 1  # Decrease the radius of the selection circle

                # Change the selected tool after a delay
                if (ptime - ctime) > 0.8:  # If 0.8 seconds have passed
                    curr_tool = getTool(x)  # Get the current tool based on x-coordinate
                    print("Selected tool: ", curr_tool)  # Print the selected tool
                    time_init = True  # Reset the time initialization flag
                    rad = 40  # Reset the radius for the selection circle

            else:
                # Reset the tool selection process if the finger is not in the tool area
                time_init = True
                rad = 40

            # Drawing based on the selected tool
            if curr_tool == "Draw":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)  # Get coordinates of the middle finger
                y9 = int(i.landmark[9].y * 480)  # Get coordinates of the index finger

                if index_raised(yi, y9):  # Check if the index finger is raised
                    # Draw on the mask
                    cv2.line(mask, (prevx, prevy), (x, y), 0, thick)  # Draw a line on the mask
                    prevx, prevy = x, y  # Update previous coordinates
                else:
                    prevx = x  # Update previous x coordinate
                    prevy = y  # Update previous y coordinate

            elif curr_tool == "Straight Line":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    if not var_inits:  # If line variables are not initialized
                        xii, yii = x, y  # Initialize starting point for the line
                        var_inits = True  # Set initialization flag to true
                    cv2.line(frm, (xii, yii), (x, y), (50, 152, 255), thick)  # Draw the line on the frame
                else:
                    if var_inits:  # If line was being drawn
                        cv2.line(mask, (xii, yii), (x, y), 0, thick)  # Draw line on the mask
                        var_inits = False  # Reset initialization flag

            elif curr_tool == "Square":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    if not var_inits:  # If square variables are not initialized
                        xii, yii = x, y  # Initialize starting point for the square
                        var_inits = True  # Set initialization flag to true
                    cv2.rectangle(frm, (xii, yii), (x, y), (0, 255, 255), thick)  # Draw square on the frame
                else:
                    if var_inits:  # If square was being drawn
                        cv2.rectangle(mask, (xii, yii), (x, y), 0, thick)  # Draw square on the mask
                        var_inits = False  # Reset initialization flag

            elif curr_tool == "Circle":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):
                    if not var_inits:  # If circle variables are not initialized
                        xii, yii = x, y  # Initialize center for the circle
                        var_inits = True  # Set initialization flag to true
                    cv2.circle(frm, (xii, yii), int(((xii - x) ** 2 + (yii - y) ** 2) ** 0.5), (255, 255, 0), thick)  # Draw circle on the frame
                else:
                    if var_inits:  # If circle was being drawn
                        cv2.circle(mask, (xii, yii), int(((xii - x) ** 2 + (yii - y) ** 2) ** 0.5), (0, 255, 0), thick)  # Draw circle on the mask
                        var_inits = False  # Reset initialization flag

            elif curr_tool == "Eraser":
                xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
                y9 = int(i.landmark[9].y * 480)

                if index_raised(yi, y9):  # Check if index finger is raised
                    cv2.circle(frm, (x, y), 70, (0, 0, 0), -1)  # Draw an eraser effect on the frame
                    cv2.circle(mask, (x, y), 70, 255, -1)  # Erase the drawing in the mask

    # Apply the mask to the frame to show the drawing
    op = cv2.bitwise_and(frm, frm, mask=mask)
    frm[:, :, 1] = op[:, :, 1]  # Update green channel
    frm[:, :, 2] = op[:, :, 2]  # Update red channel

    # Blend the tools image into the frame
    frm[:max_y, ml:max_x] = cv2.addWeighted(tools, 0.7, frm[:max_y, ml:max_x], 0.3, 0)

    # Display the currently selected tool
    cv2.putText(frm, curr_tool, (270 + ml, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Drawing Application", frm)  # Show the frame in a window

    if cv2.waitKey(1) == 27:  # EXIT >>> ESC Key 
        cv2.destroyAllWindows()  # Close all OpenCV windows
        cap.release()  # Release the video capture object
        break  # Exit the loop
