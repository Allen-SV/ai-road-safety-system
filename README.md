# AI Road Safety Monitoring System 🚦

An AI-powered traffic monitoring system that uses computer vision to detect traffic violations, road hazards, and accidents in real time using existing CCTV cameras.

The system automatically identifies unsafe driving behavior and sends alerts with evidence, helping authorities take preventive action and improve road safety.

---

## 🚀 Features

### Vehicle Detection & Tracking

Detects and tracks vehicles in real time using YOLO object detection.

### Helmet Detection

Identifies riders who are not wearing helmets.

### Overspeed Detection

Calculates vehicle speed and detects overspeeding vehicles.

### Pothole Detection

Detects potholes on roads to alert authorities for maintenance.

### Crash Detection

Identifies potential accidents from unusual vehicle movements.

### Evidence Alerts

Automatically sends alerts with evidence images through email.

---

## 🧠 Technologies Used

* Python
* YOLOv8
* OpenCV
* Computer Vision
* Email SMTP Alerts

---

## 📂 Project Structure

```
Hackathon/
│
├── app.py                # Main application
├── tracker.py            # Vehicle tracking logic
├── violation.py          # Overspeed & helmet violation detection
├── crash_detection.py    # Crash detection module
├── email_alert.py        # Sends email alerts with evidence
│
├── yolov8n.pt            # Vehicle detection model
├── best.pt               # Helmet detection model
├── pothole_yolo.pt       # Pothole detection model
│
├── road.mp4              # Test video
├── traffic.mp4           # Test video
│
└── requirements.txt      # Required Python libraries
```

---

## ⚙️ Installation

1. Clone the repository

```
git clone https://github.com/YOUR-USERNAME/AI-Road-Safety-System.git
```

2. Navigate to the project folder

```
cd AI-Road-Safety-System
```

3. (Optional but recommended) Create a virtual environment

```
python -m venv .venv
```

Activate it:

**Windows (PowerShell):**

```
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies

```
pip install -r requirements.txt
```

5. Install Streamlit (if not included)

```
pip install streamlit
```


---

## ▶️ Running the Project (Web App)

Run the Streamlit application:

```
python -m streamlit run app.py
```

After running, open your browser and go to:

```
http://localhost:8501
```

The system will process the video feed and detect violations in real time.

---

## 🖥️ How to Use

1. Upload a traffic video using the interface

2. The system will process the video

3. Detected objects and violations will be displayed in real time

4. Alerts and analysis will be generated automatically

---

## ⚠️ Notes

* Ensure model files (.pt) are present in the project directory

* Large video files may take time to process

* For best performance, use a system with GPU support

---

## 🎯 Applications

* Smart traffic monitoring
* Automated violation detection
* Road hazard identification
* Smart city infrastructure
* Accident prevention systems

---

## 👥 Team

Developed as part of a Hackathon Project.

Team Members:

* Allen Shaji Varghese
* Aben Oommen Vaidyan
* Chris Sebastian

---

## 📌 Future Improvements

* Number plate recognition
* Automatic challan generation
* Integration with traffic control systems
* Live CCTV feed processing
* Mobile dashboard for authorities

---

## 📜 License

This project is created for educational and hackathon purposes.
