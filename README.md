# Drawing Application with Hand Tracking

## Overview
This is a real-time drawing application that uses MediaPipe's hand tracking capabilities and OpenCV for computer vision tasks. Users can draw shapes and lines on the screen by selecting tools with their hands, making it an interactive and engaging experience.

## Features
- **Hand Tracking**: Utilizes MediaPipe to detect hand movements and gestures.
- **Tool Selection**: Users can choose from various drawing tools using hand positions:
  - Straight Line
  - Square
  - Circle
  - Free Drawing
  - Eraser
- **Real-Time Drawing**: Users can draw directly on the screen while seeing their actions reflected immediately.

## Requirements
To run this application, ensure you have the following libraries installed:
- [MediaPipe](https://pypi.org/project/mediapipe/)
- [OpenCV](https://pypi.org/project/opencv-python/)
- [NumPy](https://numpy.org/)

You can install these libraries using pip:
```bash
pip install mediapipe opencv-python numpy
##Usage
Clone the repository or download the code.
Make sure your webcam is connected and working.
Run the Python script:
python drawing_application.py
Use your hand to select a tool from the left side of the screen and start drawing!

##Controls
Select Tool: Position your index finger within the tool selection area to choose a drawing tool.
Draw Shapes: Use the corresponding tool to draw shapes or freehand on the canvas.
Erase: Select the eraser tool to remove any drawings.

##Screenshots
<!-- Replace with an actual screenshot of your application -->

##Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please create an issue or submit a pull request.

##License
This project is licensed under the MIT License. See the LICENSE file for more details.

##Acknowledgments
MediaPipe for providing the hand tracking framework.
OpenCV for powerful image processing capabilities.

### Notes:
- Make sure to replace `screenshot.png` with the actual screenshot file of your application.
- You can add a `LICENSE` file to your repository if you haven't done so already, and make sure to link it properly in the README.
- Feel free to adjust any sections to better suit your project!
