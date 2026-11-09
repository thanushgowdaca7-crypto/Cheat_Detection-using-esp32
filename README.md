# 🤖 AI Proctor – ESP32-Based AI Anti-Cheating Detection System

<p align="center">
  <strong>Bringing Artificial Intelligence and Embedded Systems Together</strong>
  <br/>
  A computer-vision-based monitoring prototype using Python, OpenCV, MediaPipe and ESP32.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/ESP32-WROOM-red?logo=espressif&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/MediaPipe-Face%20Mesh-blue" />
</p>

---

## 📌 About the Project

**Can an AI system detect when someone looks away during an examination?**

AI Proctor is an experimental AI-powered anti-cheating detection system that combines computer vision with embedded hardware to monitor a person's head orientation in real time.

The system uses a laptop webcam to capture video frames. Python processes these frames using OpenCV and MediaPipe to detect facial landmarks and estimate head orientation.

Based on the detection result, commands are sent to an ESP32 WROOM through serial communication. The ESP32 controls two LEDs to indicate the person's status.

The project demonstrates how AI-based computer vision can interact with physical hardware to create a real-time monitoring prototype.

### 🎯 Project Objectives

- Explore real-time facial landmark detection.
- Estimate head orientation using computer vision.
- Integrate Python-based AI processing with ESP32 hardware.
- Build a physical LED-based status indication system.
- Demonstrate communication between software and embedded hardware.

## ✨ Key Features

- 🧠 **Facial Landmark Detection:** Uses MediaPipe Face Mesh to identify facial landmarks.
- 👀 **Head Pose Estimation:** Estimates whether the person is facing the camera or turning away.
- 📷 **Live Webcam Processing:** Captures and processes video frames in real time.
- ⚡ **ESP32 Integration:** Communicates detection results through serial communication.
- 🟢 **Normal Status:** Green LED indicates the person is facing the camera.
- 🔴 **Alert Status:** Red LED indicates a turned-away head, missing face or multiple faces.
- 💻 **Python-Based AI:** Uses OpenCV, MediaPipe and NumPy for processing.

## ⚙️ System Architecture

```text
       LAPTOP WEBCAM
             |
             v
       PYTHON APPLICATION
             |
             v
       OPENCV PROCESSING
             |
             v
       MEDIAPIPE FACE MESH
             |
             v
       HEAD POSE ESTIMATION
             |
             v
       DETECTION DECISION
             |
             v
      SERIAL COMMUNICATION
             |
             v
          ESP32 WROOM
             |
        +----+----+
        |         |
        v         v
    GREEN LED   RED LED
     NORMAL      ALERT
```

## 🚦 Detection Logic

The system evaluates the webcam feed and determines the current detection state.

| Detection Condition | System Response |
|---|---|
| One face detected and facing camera | 🟢 Green LED ON |
| Head turned away | 🔴 Red LED ON |
| No face detected | 🔴 Red LED ON |
| Multiple faces detected | 🔴 Red LED ON |

### Serial Communication

Python sends commands to the ESP32 using USB serial communication.

| Command | ESP32 Action |
|---|---|
| `G` | Green LED ON |
| `R` | Red LED ON |
| `N` | Both LEDs OFF |

## 🧰 Hardware Requirements

| Component | Quantity |
|---|---:|
| ESP32 WROOM Development Board | 1 |
| Red LED | 1 |
| Green LED | 1 |
| 220Ω / 330Ω Resistors | 2 |
| Jumper Wires | As required |
| USB Cable | 1 |
| Laptop with Webcam | 1 |

## 🔌 Circuit Connections

| Component | ESP32 GPIO |
|---|---|
| Green LED Anode (+) | GPIO 25 through resistor |
| Red LED Anode (+) | GPIO 26 through resistor |
| Both LED Cathodes (-) | GND |

**Note:** Connect a current-limiting resistor in series with each LED.

## 💻 Software Requirements

- Python
- Arduino IDE
- OpenCV
- MediaPipe
- NumPy
- PySerial

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Proctor.git
cd AI-Proctor
```

### 2. Install Dependencies

```bash
py -m pip install opencv-python==4.10.0.84 mediapipe==0.10.21 numpy==1.26.4 pyserial
```

### 3. Upload ESP32 Firmware

1. Open `ESP32_Anti_Cheating.ino` in Arduino IDE.
2. Select your ESP32 board.
3. Select the correct COM port.
4. Upload the firmware.
5. Close the Arduino Serial Monitor.

### 4. Configure the Serial Port

Open `anti_cheating_cv.py` and check the serial port configuration.

```python
SERIAL_PORT = "COM7"
BAUD_RATE = 115200
```

Change the COM port according to your ESP32 connection.

### 5. Run the Application

```bash
py anti_cheating_cv.py
```

The webcam will open and begin processing frames.

Press **Q** to exit the application.

## 🧪 Technologies Used

| Technology | Application |
|---|---|
| Python | Main application logic |
| OpenCV | Image processing and head pose estimation |
| MediaPipe | Facial landmark detection |
| NumPy | Numerical calculations |
| PySerial | Serial communication |
| ESP32 WROOM | LED control and hardware interaction |
| Arduino IDE | ESP32 firmware development |

## ⚠️ Limitations

- This is an experimental prototype, not a production-ready examination monitoring system.
- Head pose estimation does not directly measure eye gaze.
- Looking away does not necessarily indicate cheating.
- Lighting, camera position and facial orientation can affect detection.
- The system should not be used for disciplinary decisions without human verification.

## 🔮 Future Enhancements

- Eye gaze tracking.
- Improved head pose estimation.
- Real-time event logging.
- Multiple-person monitoring.
- Web-based monitoring dashboard.
- Notification and alert integration.

---

## 🎥 Video Demonstration & References

Want to see the project working? Watch the actual demonstration.

<p align="center">
  <a href="https://youtube.com/shorts/oU2ydZBXqRk?si=iJRBICJOCFHyyQ_6">
    <img src="https://img.shields.io/badge/▶%20Watch%20AI%20Proctor%20Demo-FF0000?style=for-the-badge&logo=youtube&logoColor=white">
  </a>
</p>

### 📺 More Project Videos

This project is part of the **EmbedX** electronics and embedded systems project series.

Visit the channel to explore more demonstrations, ESP32 experiments, AI integrations, hardware builds and practical electronics projects.

<p align="center">
  <a href="https://youtube.com/@embedx-1?si=PDrEQLf2UmA2KQzc">
    <img src="https://img.shields.io/badge/Explore%20More%20Projects%20on%20YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white">
  </a>
</p>

## 🌐 Connect With EmbedX

Follow EmbedX for more projects, tutorials, experiments and updates.

<p align="center">
  <a href="YOUR_INSTAGRAM_LINK">
    <img src="https://img.shields.io/badge/Instagram-Follow-E4405F?style=for-the-badge&logo=instagram&logoColor=white">
  </a>
  <a href="YOUR_X_LINK">
    <img src="https://img.shields.io/badge/X-Follow-black?style=for-the-badge&logo=x&logoColor=white">
  </a>
  <a href="YOUR_REDDIT_LINK">
    <img src="https://img.shields.io/badge/Reddit-Join-FF4500?style=for-the-badge&logo=reddit&logoColor=white">
  </a>
  <a href="https://youtube.com/@embedx-1?si=PDrEQLf2UmA2KQzc">
    <img src="https://img.shields.io/badge/YouTube-Subscribe-FF0000?style=for-the-badge&logo=youtube&logoColor=white">
  </a>
</p>

---

<p align="center">
  **Built with curiosity. Powered by technology.**
  <br/>
  <strong>EmbedX – Build Beyond Boards.</strong>
  <br/>
  ⭐ If you find this project useful, consider giving this repository a star!
</p>
