# 🚗 Monocular Vehicle Speed Estimation Using YOLO-Based Detection and Line-Crossing Temporal Analysis

A real-time vehicle speed estimation system built using computer vision and deep learning techniques on monocular traffic video streams. The system detects, tracks, and estimates vehicle speeds without requiring specialized hardware such as radar or LIDAR.

---

## 🔍 Key Features

- **Vehicle Detection:** Real-time detection using YOLO (You Only Look Once)  
- **Multi-Object Tracking:** IoU-based tracking for maintaining vehicle identity across frames  
- **Speed Estimation:** Line-crossing temporal analysis using virtual reference zones  
- **Performance:** ~92.5% detection accuracy with ±5% speed estimation error  
- **Web Interface:** Upload videos, visualize detections, and analyze speed violations  
- **Real-Time Processing:** Optimized pipeline for continuous video stream analysis  

---

## ⚙️ System Overview

The system processes video input frame-by-frame to:

1. Detect vehicles using a YOLO-based deep learning model  
2. Track detected vehicles across frames using IoU-based association  
3. Measure the time taken for vehicles to cross predefined virtual reference lines  
4. Compute vehicle speed based on temporal displacement  
5. Flag vehicles exceeding a user-defined speed threshold  

This approach provides a **scalable and cost-effective alternative** to traditional speed detection systems by leveraging existing CCTV infrastructure.

---

## 🧠 Methodology

- **Detection:** YOLO-based object detection  
- **Tracking:** Lightweight IoU-based multi-object tracking  
- **Speed Computation:**
  - Define two virtual reference lines in the scene  
  - Measure time taken for a vehicle to traverse between them  
  - Compute speed using temporal analysis  

---

## 🏗️ Project Structure
