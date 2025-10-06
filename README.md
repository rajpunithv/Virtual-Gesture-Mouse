# 🖐️ Virtual Gesture Mouse

**Virtual Gesture Mouse** is an AI-powered project that allows users to **control the computer mouse using hand gestures**.  
It uses a webcam to detect hand landmarks in real-time and maps them to actions like **move**, **click**, and **scroll** — all without touching a physical mouse.

---

## 🚀 Features

- 🎯 **Cursor Control:** Move the mouse pointer with your **index finger**.  
- 👆 **Left Click:** Tap **thumb + index** fingers together.  
- 🤏 **Right Click:** Tap **thumb + index + middle** fingers together.  
- 🖐️ **Scroll Up:** Open **four fingers** (excluding thumb).  
- ✊ **Scroll Down:** Close **four fingers** (excluding thumb).  
- ⚙️ **Smooth Tracking:** Uses Mediapipe’s advanced hand-tracking for precise and real-time response.

---

## 🧠 Technologies Used

- **Python 3.8+**  
- **OpenCV** – Real-time image and video processing  
- **MediaPipe** – Hand landmark detection and tracking  
- **PyAutoGUI** – For performing mouse actions  
- **NumPy** – For numerical and smoothing operations  

---

## ⚙️ Requirements

Make sure Python 3.8 or above is installed, then install these libraries:

```bash
pip install opencv-python mediapipe pyautogui numpy
