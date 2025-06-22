import cv2
import mediapipe as mp
import time
import math
import datetime
from multiprocessing import Value
import pyttsx3

# Set up text-to-speech engine once
engine = pyttsx3.init()
engine.setProperty('rate', 170) 

mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def distance(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

def eye_aspect_ratio(landmarks, eye_indices):
    p1, p2, p3, p4, p5, p6 = [landmarks[i] for i in eye_indices]
    vertical1 = distance(p2, p6)
    vertical2 = distance(p3, p5)
    horizontal = distance(p1, p4)
    return (vertical1 + vertical2) / (2.0 * horizontal)

def get_eye_gaze_center(landmarks):
    left_center = (landmarks[33].x + landmarks[133].x) / 2
    right_center = (landmarks[362].x + landmarks[263].x) / 2
    return (left_center + right_center) / 2

def is_thumbs_up(hand_landmarks):
    # Thumb tip: 4, Thumb MCP: 2
    # Index tip: 8, Index MCP: 5
    # Middle tip: 12, MCP: 9
    # Ring tip: 16, MCP: 13
    # Pinky tip: 20, MCP: 17
    tips = [4, 8, 12, 16, 20]
    mcp = [2, 5, 9, 13, 17]

    extended = []
    for tip, base in zip(tips, mcp):
        tip_y = hand_landmarks.landmark[tip].y
        base_y = hand_landmarks.landmark[base].y
        extended.append(tip_y < base_y)  # True if finger is extended

    return extended[0] and not any(extended[1:])  # Only thumb is up

def log_action(action):
    # Log to file
    with open("log.txt", "a", encoding="utf-8") as log:
        log.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {action}\n")

    # Speak the action aloud
    engine.say(action)
    engine.runAndWait()

def is_thumbs_up(hand_landmarks):
    # Tip and base for each finger
    tip_ids = [4, 8, 12, 16, 20]
    mcp_ids = [2, 5, 9, 13, 17]

    # Get y values of all finger tips and their base joints
    is_thumb_up = hand_landmarks.landmark[4].y < hand_landmarks.landmark[2].y
    other_fingers_down = all(
        hand_landmarks.landmark[tip].y > hand_landmarks.landmark[mcp].y
        for tip, mcp in zip(tip_ids[1:], mcp_ids[1:])
    )

    return is_thumb_up and other_fingers_down

def start_eye_control(status_text, blink_flag, track_text):
    cap = cv2.VideoCapture(0)

    last_hand_time = time.time() - 1
    last_gaze_time = time.time() - 1

    is_playing = False
    current_track = 1

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result_face = face_mesh.process(frame_rgb)
        result_hands = hands.process(frame_rgb)

        # Face / Gaze detection
        if result_face.multi_face_landmarks:
            for face_landmarks in result_face.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION
                )

                eye_center = get_eye_gaze_center(landmarks)
                now = time.time()

                if now - last_gaze_time > 1:
                    if eye_center < 0.4:
                        current_track = max(1, current_track - 1)
                        status_text.value = 2  # Previous
                        track_text.value = current_track
                        log_action("Gaze Left -> Previous Track")
                        last_gaze_time = now
                    elif eye_center > 0.6:
                        current_track += 1
                        status_text.value = 3  # Next
                        track_text.value = current_track
                        log_action("Gaze Right -> Next Track")
                        last_gaze_time = now

        # Thumbs up detection
        if result_hands.multi_hand_landmarks:
            now = time.time()
            if now - last_hand_time > 1:
                for hand_landmarks in result_hands.multi_hand_landmarks:
                    if is_thumbs_up(hand_landmarks):
                        is_playing = not is_playing
                        action = "Play" if is_playing else "Pause"
                        status_text.value = 1
                        blink_flag.value = 1
                        track_text.value = current_track
                        log_action(f"Thumbs Up -> {action}")
                        last_hand_time = now
                    else:
                        blink_flag.value = 0

                for hand_landmark in result_hands.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame, hand_landmark, mp_hands.HAND_CONNECTIONS
                    )

        cv2.imshow("Live Control Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    

    cap.release()
    cv2.destroyAllWindows()
