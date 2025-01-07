import cv2
from pynput.keyboard import Controller
keyboard = Controller()

def detect_gaze():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        return
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    print("Press 'Q' to exit the program.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from the webcam.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        frame_width = frame.shape[1]

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            face_center = x + w // 2
            if face_center < frame_width // 3:
                print("Previous Track")
                keyboard.press('b') 
                keyboard.release('b')
            elif face_center > 2 * frame_width // 3:
                print("Next Track")
                keyboard.press('n') 
                keyboard.release('n')
            else:
                print("Play/Pause")
                keyboard.press('p') 
                keyboard.release('p')

        cv2.imshow('Eye Tracker - Multimedia Control', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_gaze()