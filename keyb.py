import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hand solution
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Define the virtual keyboard layout
keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

# Function to draw the virtual keyboard
def draw_keyboard(image, keys, pressed_key, key_pressed_string):
    h, w, _ = image.shape
    key_h, key_w = 50, 50
    margin = 10
    
    # Draw the virtual keyboard
    for i, row in enumerate(keys):
        for j, key in enumerate(row):
            x = j * (key_w + margin) + margin
            y = i * (key_h + margin) + margin
            color = (0, 255, 0) if key != pressed_key else (0, 0, 255)
            cv2.rectangle(image, (x, y), (x + key_w, y + key_h), color, 2)
            cv2.putText(image, key, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    # Draw the pressed key display area
    if pressed_key:
        cv2.putText(image, f"Key Pressed: {pressed_key}", (20, h - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the key pressed string at the bottom
    cv2.putText(image, f"Keys Pressed: {key_pressed_string}", (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

# Initialize the video capture
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    pressed_key = None
    key_pressed_list = []
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally for a later selfie-view display
        image = cv2.flip(image, 1)
        image_height, image_width, _ = image.shape

        # Convert the BGR image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image and detect hands
        results = hands.process(image_rgb)

        # Draw the virtual keyboard
        key_pressed_string = ' '.join(key_pressed_list)
        draw_keyboard(image, keys, pressed_key, key_pressed_string)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get the index finger tip and thumb tip coordinates
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                
                x_index = int(index_finger_tip.x * image_width)
                y_index = int(index_finger_tip.y * image_height)
                x_thumb = int(thumb_tip.x * image_width)
                y_thumb = int(thumb_tip.y * image_height)
                
                # Draw circles at the finger tips
                cv2.circle(image, (x_index, y_index), 10, (0, 255, 0), -1)
                cv2.circle(image, (x_thumb, y_thumb), 10, (255, 0, 0), -1)

                # Check if two fingers are close to each other (click gesture)
                distance = np.sqrt((x_index - x_thumb) ** 2 + (y_index - y_thumb) ** 2)
                if distance < 30:  # Adjust threshold as needed
                    # Determine the pressed key
                    key_pressed = None
                    for i, row in enumerate(keys):
                        for j, key in enumerate(row):
                            key_x = j * (50 + 10) + 10
                            key_y = i * (50 + 10) + 10
                            if key_x < x_index < key_x + 50 and key_y < y_index < key_y + 50:
                                key_pressed = key
                                break
                        if key_pressed:
                            break
                    
                    if key_pressed:
                        pressed_key = key_pressed
                        if pressed_key not in key_pressed_list:
                            key_pressed_list.append(pressed_key)
                else:
                    pressed_key = None

        # Display the resulting frame
        cv2.imshow('Gesture Virtual Keyboard', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

# Release the capture and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()
