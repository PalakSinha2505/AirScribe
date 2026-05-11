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
