import cv2
import numpy as np
import mediapipe as mp
from collections import deque

# --- CONFIGURATION (Settings) ---
# Alag-alag colors ke liye arrays (Blue, Green, Red, Yellow)
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# Indexes taaki hum points ko track kar sakein
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# Colors (BGR Format in OpenCV)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0 # Default Blue hai

# --- MEDIAPIPE SETUP (Haath detect karne wala tool) ---
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Webcam On karo
cap = cv2.VideoCapture(0)

print("Project Start ho gaya! 'q' dabayein band karne ke liye.")
print("Colors change karne ke liye keys dabayein: b (Blue), g (Green), r (Red), y (Yellow)")
print("Sab mitane ke liye: c (Clear)")

while True:
    # Frame read karo
    ret, frame = cap.read()
    if not ret:
        break

    # Frame ko flip karo (Mirror effect)
    frame = cv2.flip(frame, 1)
    
    # Image ko RGB mein convert karo (Mediapipe ke liye zaroori hai)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Haath detect karo
    result = hands.process(framergb)
    
    # Ungli ki position dhoondo
    center = None
    if result.multi_hand_landmarks:
        landmarks = result.multi_hand_landmarks[0].landmark
        
        # Point 8 = Index Finger Tip (Ungli ka nakhun wala hissa)
        # Humein coordinates (x, y) chahiye screen ke hisaab se
        h, w, c = frame.shape
        cx, cy = int(landmarks[8].x * w), int(landmarks[8].y * h)
        center = (cx, cy)
        
        # Haath par lines draw karo (dikhne mein cool lagta hai)
        mpDraw.draw_landmarks(frame, result.multi_hand_landmarks[0], mpHands.HAND_CONNECTIONS)

    # --- KEYBOARD CONTROLS (Rang badalne ke liye) ---
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"): break # Quit
    elif key == ord("c"): # Clear All
        bpoints = [deque(maxlen=512)]
        gpoints = [deque(maxlen=512)]
        rpoints = [deque(maxlen=512)]
        ypoints = [deque(maxlen=512)]
        blue_index = 0; green_index = 0; red_index = 0; yellow_index = 0
        
    elif key == ord("b"): colorIndex = 0 # Blue
    elif key == ord("g"): colorIndex = 1 # Green
    elif key == ord("r"): colorIndex = 2 # Red
    elif key == ord("y"): colorIndex = 3 # Yellow

    # --- DRAWING LOGIC ---
    # Agar ungli detect hui hai, toh us point ko list mein daalo
    if center:
        if colorIndex == 0: bpoints[blue_index].appendleft(center)
        elif colorIndex == 1: gpoints[green_index].appendleft(center)
        elif colorIndex == 2: rpoints[red_index].appendleft(center)
        elif colorIndex == 3: ypoints[yellow_index].appendleft(center)
    else:
        # Agar ungli hat gayi, toh naya stroke shuru karo (juda hua na ho)
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # --- SABHI POINTS KO SCREEN PAR DRAW KARO ---
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                # Line draw karo
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 5)

    # Screen dikhao
    cv2.imshow("Air Canvas - By You", frame)

# Safayi se band karo
cap.release()
cv2.destroyAllWindows()