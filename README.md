# **Motion Detection and Alert System**

A Python-based motion detection system that captures images when motion is detected and sends email alerts. The system also manages storage by automatically deleting images older than 10 days.

---

## **Features**
- Detects motion using a webcam.
- Sends email alerts when motion is detected.
- Captures and saves images during motion events.
- Automatically deletes images older than 10 days to save storage space.

---

## **Technologies Used**
- Python
- OpenCV (Computer Vision)
- SMTP (Email Integration)
- Operating System (File Management)

---

## **Requirements**

1. Python 3.7+
2. Required Python Libraries:
   - `cv2` (OpenCV)
   - `numpy`
   - `smtplib`
   - `email`
3. Webcam

---

## **Setup and Usage**

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/motion-detection-alert.git
   cd motion-detection-alert
