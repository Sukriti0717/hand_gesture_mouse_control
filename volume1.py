import cv2
import mediapipe as mp
import pyautogui as pg

x1=y1=x2=y2=0

#opening webcam
webcam=cv2.VideoCapture(0)

#hand object, and to draw points on our hands
my_hands=mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

#displaying webcam image
while True:
    #capturing the image in two variables
    _ , image = webcam.read()
    image = cv2.flip(image, 1) #flipped about y-axis
    frame_height, frame_width , _ = image.shape #depth

    #showing it in a window
    #cv2.imshow("Hand volume control using python", image)

    #to draw points, we need to convert bgr image to rgb image
    rgb_image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #to process hands
    output = my_hands.process(rgb_image)
    #function also identifies multiple hands, to collect all:
    hands = output.multi_hand_landmarks
    #drawing points for all hands
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            #now for controlling the volume:
            landmarks=hand.landmark
            for id, landmark in enumerate(landmarks):
                x=int(landmark.x * frame_width)
                y=int(landmark.y * frame_height)
                if id==8: #forefinger
                    cv2.circle(img=image, center=(x,y), radius=8, color=(0,255,255), thickness=3)
                    x1 = x
                    y1 = y
                if id==4: #thumb
                    cv2.circle(img=image, center=(x,y), radius=8, color=(0,0,255), thickness=3) #bgr color
                    x2 = x
                    y2 = y
                # distance to increase-decrease, eucledian
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (0.5) // 4
        cv2.line(image, (x1,y1), (x2,y2), (255,0,0), 5)
        if dist>30:
            pg.press("volumeup")
        else:
            pg.press("volumedown")

    cv2.imshow("Hand Volume Control Using Python", image)

    #capture every 10 milliseconds to appear as video
    #cv2.waitKey(10)
    #we need to close window too

    key=cv2.waitKey(10)
    if key == 27: #escape key
        break

webcam.release()
cv2.destroyAllWindows()

