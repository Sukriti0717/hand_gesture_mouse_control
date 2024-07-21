import cv2
import mediapipe as mp
import pyautogui as pg

capture_hands = mp.solutions.hands.Hands()
drawing_options = mp.solutions.drawing_utils

screen_width, screen_height = pg.size()

camera = cv2.VideoCapture(0)
x1=x2=y1=y2=0
while True:
    _, image = camera.read()
    image_height, image_width, _ = image.shape
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output_hands = capture_hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            drawing_options.draw_landmarks(image, hand)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)
                # print(lm.x, lm.y)
                if id==8:
                    mouse_x = int(screen_width/image_width * x)
                    mouse_y = int(screen_height / image_height * y)
                    cv2.circle(image, (x, y), 5, (0, 255, 255))
                    pg.moveTo(mouse_x, mouse_y)
                    x1=x
                    y1=y
                if id == 4:
                    x2=x
                    y2=y
                    cv2.circle(image, (x, y), 5, (0, 255, 255))
        dist = y2 - y1 #vertical distance
        #print(dist)
        if dist<20:
            pg.click()
            print("Clicked")
    cv2.imshow("Hand Movement Video Capture", image)
    key = cv2.waitKey(10)
    if key==27:
        break
camera.release()
cv2.destroyAllWindows()
