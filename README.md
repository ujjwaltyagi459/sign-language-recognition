# Sign Language Recognition

A real-time hand gesture recognition system built with Python, OpenCV, and MediaPipe that detects and classifies basic sign language gestures using a webcam feed.

## 📌 Features

- Real-time hand tracking using webcam input
- Detects 21 hand landmarks per hand using MediaPipe
- Classifies finger positions (up/down) to recognize gestures
- Supports both left and right hand detection
- Displays the detected sign directly on the video feed
- Includes debug overlay showing individual finger states

## ✋ Supported Gestures

| Gesture | Hand Position |
|---------|---------------|
| **Hello** | Thumb and pinky raised, others down |
| **Thank You** | Index and middle fingers raised, others down |
| **Yes** | Only index finger raised |
| **No** | All fingers raised |

## 🛠️ Tech Stack

- **Language:** Python
- **Libraries:** OpenCV, MediaPipe, NumPy
- **Concepts Used:** Computer Vision, Hand Landmark Detection, Real-time Video Processing, Gesture Classification Logic

## 🚀 How to Run

1. Clone the repository
   ```bash
   git clone https://github.com/ujjwaltyagi459/sign-language-recognition.git
   ```
2. Navigate to the project folder
   ```bash
   cd sign-language-recognition
   ```
3. Install the required dependencies
   ```bash
   pip install opencv-python mediapipe numpy
   ```
4. Run the script
   ```bash
   python mp.py
   ```
5. Press **`q`** to quit the detection window.

## 📂 Project Structure

```
sign-language-recognition/
│
├── mp.py          # Main script - hand tracking and gesture classification
└── README.md      # Project documentation
```

## ⚙️ How It Works

1. Captures live video from the webcam using OpenCV.
2. Passes each frame to MediaPipe's Hands solution to detect 21 hand landmarks.
3. Compares the Y-coordinates of fingertip landmarks against their respective joint landmarks to determine if each finger is raised.
4. Applies gesture-matching rules based on which fingers are up to classify the sign.
5. Overlays the detected gesture and debug info on the live video feed.

## 🎯 What I Learned

Building this project helped me strengthen my understanding of:
- Computer vision fundamentals using OpenCV
- Real-time hand landmark detection with MediaPipe
- Translating raw landmark coordinates into meaningful gesture logic
- Processing and interpreting live camera feed data in real time

## 🔮 Future Improvements

- Expand gesture vocabulary beyond the current 4 signs
- Add support for two-handed gestures
- Train a machine learning classifier for more robust recognition
- Convert detected signs to speech output

## 👤 Author

**Ujjwal Tyagi**
B.Tech Computer Science (IoT), Raj Kumar Goel Institute of Technology, Ghaziabad

---

⭐ If you found this project useful, consider giving it a star!
