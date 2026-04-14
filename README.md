# 📏 AR-Distance-Measurement-Android

An Augmented Reality (AR) based Android application that allows users to measure real-world distances using their smartphone camera.

---
 🚀 Real-time distance measurement using ARCore with 3D spatial tracking

 🚀 Built using ARCore + Sceneform for real-time spatial measurement

## 🚀 Features

 * 📐 Measure distance between two real-world points
 * 🎯 Real-time crosshair targeting system
 * 📱 Uses ARCore for environment tracking
 * 🔄 Reset and re-measure functionality
 * ⚡ Live distance calculation in centimeters

---

## 🧠 How It Works

The app uses **ARCore** to detect planes and track device motion.

1. User points camera at a surface
2. First point is locked using center reticle
3. Second point updates dynamically as user moves
4. Distance is calculated using 3D coordinate difference

---

## 🧩 Technical Implementation

* Uses ARCore HitTest to detect real-world surfaces
* Places anchor points in 3D space using camera tracking
* Retrieves world coordinates (x, y, z) of selected points
* Computes distance using Euclidean Distance Formula:

distance = √[(x2 - x1)² + (y2 - y1)² + (z2 - z1)²]

* Sceneform renders visual feedback and measurement line in AR space

---

## 📊 Tech Stack

 * Kotlin
 * Android Studio
 * ARCore SDK
 * Sceneform (3D rendering)

---

## 📷 Demo
![WhatsApp Image 2026-04-13 at 12 14 57 AM](https://github.com/user-attachments/assets/7d73d0b5-4111-4012-80cd-0b5401b1516f)
![WhatsApp Image 2026-04-13 at 12 15 02 AM](https://github.com/user-attachments/assets/2d6fb965-c6ea-460a-9f8e-2d8d39c54179)

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/kushjainv1903/AR-Measurement-Tape.git
```

2. Open in Android Studio

3. Connect ARCore-supported device

4. Run the app

---

## ⚠️ Requirements

* ARCore supported device
* Camera permission enabled

---

## 📌 Future Improvements

* Object detection integration (YOLO)
* Area and volume measurement
* Measurement history saving
* Voice feedback

---

## 📄 License

This project is licensed under the MIT License.
