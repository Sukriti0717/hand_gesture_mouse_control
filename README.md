# hand_gesture_mouse_control
This project implements a hand gesture-based control system using a webcam to track and interpret hand movements, enabling users to control various functions on their computer. The project leverages computer vision and machine learning techniques to create a touchless interface, offering a novel way to interact with devices.

# Features
1. Brightness Control: Adjust the screen brightness by changing the position of your hand in front of the camera. This feature utilizes hand tracking to map hand movements to brightness levels.
2. Virtual Keyboard Control: Operate an on-screen virtual keyboard using hand gestures. This allows users to type without physically touching a keyboard, enhancing accessibility and convenience.
3. Mouse Control & Clicking Actions: Move the mouse cursor, perform left-clicks, right-clicks, and scroll actions by gesturing in front of the camera. This feature replaces traditional mouse inputs with hand movements.
4. Volume Control: Increase or decrease the system volume by gesturing up or down with your hand. This feature provides a hands-free method to control audio levels.

# Libraries Used
- MediaPipe: A cross-platform framework used for building pipelines to process perceptual data, such as hand and face tracking.
- OpenCV (cv2):A powerful library for computer vision, used here to process video streams and apply image processing techniques.
- NumPy: A fundamental package for numerical computations in Python, used for handling arrays and mathematical functions.
- screen_brightness_control: A library for controlling screen brightness on different platforms.
- PyAutoGUI: A library for automating mouse and keyboard actions, used to simulate mouse clicks and keystrokes.
- math: Python's built-in mathematical functions used for various calculations within the project.

# How It Works
- Hand Detection: MediaPipe is used to detect and track hand landmarks in real-time through the webcam.
- Gesture Recognition: Specific hand gestures are recognized based on the position and orientation of the hand, and these gestures are mapped to different control actions.
- Control Functions: The recognized gestures trigger functions such as adjusting brightness, controlling the mouse, typing on the virtual keyboard, and adjusting volume.

  

