import tkinter as tk
from multiprocessing import Process, Value
from eye_control_core import start_eye_control
import threading
import time

TRACK_DURATION = 30 
def load_track_titles():
    try:
        with open("tracks.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return ["Track 1", "Track 2", "Track 3"]

def dashboard_gui(status_text, blink_flag, track_text):
    root = tk.Tk()
    root.title("Virtual Car Media Player")
    root.geometry("420x320")

    tk.Label(root, text="🚗 Car Dashboard", font=("Arial", 16)).pack(pady=10)

    status_label = tk.Label(root, text="Status: -", font=("Arial", 12))
    status_label.pack()

    gesture_label = tk.Label(root, text="Gesture: None", font=("Arial", 12))
    gesture_label.pack()

    track_label = tk.Label(root, text="Now Playing: -", font=("Arial", 12))
    track_label.pack()

    timer_label = tk.Label(root, text="Time Remaining: --:--", font=("Arial", 12))
    timer_label.pack(pady=5)

    progress = tk.DoubleVar()
    progress_bar = tk.Scale(root, variable=progress, from_=0, to=100,
                            orient=tk.HORIZONTAL, length=300, state='disabled')
    progress_bar.pack(pady=5)

    play_timer = {
        "playing": False,
        "remaining": TRACK_DURATION,
        "last_track": 0
    }

    track_titles = load_track_titles()

    def timer_loop():
        while True:
            if play_timer["playing"]:
                if play_timer["remaining"] > 0:
                    play_timer["remaining"] -= 1
                    percent = ((TRACK_DURATION - play_timer["remaining"]) / TRACK_DURATION) * 100
                    progress.set(percent)
                    timer_label.config(text=f"Time Remaining: 00:{play_timer['remaining']:02}")
                else:
                    play_timer["playing"] = False
                    timer_label.config(text="Track Ended")
            time.sleep(1)

    def update_gui():
        status_map = {0: "-", 1: "Play/Pause", 2: "Previous", 3: "Next"}
        gesture = "Thumbs Up" if blink_flag.value == 1 else "None"
        track_index = max(0, track_text.value - 1)

        status_label.config(text=f"Status: {status_map.get(status_text.value, '-')}")
        gesture_label.config(text=f"Gesture: {gesture}")

        track_title = track_titles[track_index] if track_index < len(track_titles) else f"Track {track_text.value}"
        track_label.config(text=f"Now Playing: {track_title}")

        if track_text.value != play_timer["last_track"]:
            play_timer["playing"] = True
            play_timer["remaining"] = TRACK_DURATION
            progress.set(0)
            play_timer["last_track"] = track_text.value

        root.after(500, update_gui)

    threading.Thread(target=timer_loop, daemon=True).start()
    update_gui()
    root.mainloop()

if __name__ == "__main__":
    status_text = Value('i', 0)
    blink_flag = Value('i', 0)
    track_text = Value('i', 0)

    p1 = Process(target=start_eye_control, args=(status_text, blink_flag, track_text))
    p1.start()

    dashboard_gui(status_text, blink_flag, track_text)
    p1.join()
