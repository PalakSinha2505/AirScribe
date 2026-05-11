# AirScribe

## Overview

AirScribe is a computer vision-based gesture control system that enables users to interact with their computer using hand movements captured through a webcam. The project leverages real-time hand tracking and gesture recognition to simulate mouse and system control operations, providing a touchless and intuitive human-computer interaction experience.

---

## Problem Statement

Traditional input devices such as keyboards and mice require physical interaction, which may not always be efficient, accessible, or hygienic in certain environments. Additionally, users with physical limitations or those working in immersive or hands-free setups often require alternative interaction methods.

AirScribe addresses the need for a real-time, vision-based interaction system that allows users to control basic computer operations using hand gestures without physical contact.

---

## Solution

AirScribe uses computer vision and machine learning-based hand landmark detection to track hand movements via a webcam. These tracked gestures are mapped to system-level actions such as cursor movement and mouse clicks. The system processes live video input, detects hand landmarks, applies smoothing techniques for stability, and translates gestures into actionable commands.

---

## Features

- Real-time hand tracking using webcam input
- Gesture-based mouse movement control
- Click simulation using predefined hand gestures
- Smoothing algorithms for stable cursor movement
- Modular architecture for tracking, control, and processing components
- Lightweight design suitable for real-time execution
- Extendable structure for adding new gestures and actions

---

## Tech Stack

- Python 3.10
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI
- PyQt5

---

## Project Structure
AirScribe/
│
├── core/
│ └── smoothing.py
│
├── control/
│ └── mouse_controller.py
│
├── tracking/
│ └── hand_tracker.py
│
├── main.py
├── requirements.txt
└── README.md


---

## Setup Instructions

### 1. Prerequisites

Ensure you have the following installed:
- Python 3.10 or above
- A working webcam

---

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/AirScribe.git
cd AirScribe
```
---
### 3. Create Virtual Environment
```bash
python -m venv venv
```
Activate it
---
### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
---
### 5. Run the file
```bash
python main.py
```
Make sure your webcam is enabled before running the application.

---

## How it Works
- Webcam captures live video stream
- MediaPipe detects hand landmarks in real time
- Hand tracking module processes finger positions
- Gesture recognition logic interprets movement patterns
- Mouse controller maps gestures to system cursor actions
- Smoothing module ensures stable cursor movement
---
## Contribution Guidelines

Contributions are welcome and encouraged.

Steps to Contribute:
### 1. Fork the repository
### 2. Create a new branch:
```bash
git checkout -b feature-name
```
### 3. Make your changes and ensure code quality
### 4. Commit your changes:
```bash
git commit -m "Add meaningful message"
```
### 5. Push to your branch:
```bash
git push origin feature-name
```
### 6. Open a Pull Request
---
## License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this project with proper attribution.

---
## Author
Palak Sinha


