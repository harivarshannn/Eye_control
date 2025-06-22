# 🎵 Gesture-Controlled Virtual Car Media Dashboard 🚗

This is a Python-based vision project that simulates a **hands-free in-car music system**. Using just your **eyes** and a **thumbs-up gesture**, you can control a media dashboard — no keyboard or mouse required!

## 🔥 Features

- 👁️ **Eye Gaze Control**
  - Look left → Previous Track
  - Look right → Next Track

- 👍 **Thumbs-Up Gesture**
  - Perform thumbs-up to toggle Play/Pause

- 🖥️ **Live GUI Dashboard**
  - Built with Tkinter
  - Shows Now Playing, Progress Bar, Timer

- 🎵 **Tamil Track Titles**
  - Reads track names from a `tracks.txt` file

- 🗣️ **Voice Feedback**
  - Announces actions using `pyttsx3` (offline TTS)

- 📋 **Logging**
  - Every action is logged to `log.txt` with timestamp

---
## 📂 Project Structure

project/
│
├── eye_control_core.py # Main logic: gaze, thumbs-up, logging, voice
├── dashboard_gui.py # Tkinter GUI for display
├── tracks.txt # Tamil track titles (editable)
├── log.txt # Auto-generated action log
└── README.md

▶️ How to Run
Clone the repository:
git clone https://github.com/your-username/virtual-car-dashboard.git
cd virtual-car-dashboard

Add your own Tamil songs to tracks.txt (one per line)

Run the app:
python dashboard_gui.py

Control using:
----->👁️ Eye Gaze → Track Switch
----->👍 Thumbs-Up → Play / Pause

📃 Sample tracks.txt
       Naan Ponnoviyā - 96
       Va Thaan Va - Master
       AvanIvan - Paradesi
       Chandhira - Thiruchitrambalam
       Mallipoo - Roja
       Chinna Chinna Aasai - Roja
      Neeyum Nalla Iru - Sarpatta

  
👨‍💻 Author
Made with ❤️ by HARIVARSHAN N
💼 LinkedIn: www.linkedin.com/in/harivarshan-n-752282299
📫 GitHub: https://github.com/harivarshannn




🏁 Future Improvements
🎙️ Add voice command support
📊 Track history GUI viewer
🔊 Volume control via hand raise
📂 Playlist loader with real audio files
