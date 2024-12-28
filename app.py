import cv2
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
from datetime import datetime, timedelta

# Email configuration
EMAIL_ADDRESS = "hasib1711@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "#### #### #### ####"
SMTP_SERVER = "smtp.gmail.com"
RECEIVER_EMAIL = "hasib1711@gmail.com"
SMTP_PORT = 587

# Function to send email alert
def send_email_alert():
    try:
        subject = "Motion Detected Alert"
        body = "Motion has been detected by your security camera!"

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server and send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        print("Email alert sent successfully.")
    except Exception as e:
        print("Failed to send email alert:", e)

# Function to delete images older than 10 days
def delete_old_images(folder, days=10):
    cutoff_date = datetime.now() - timedelta(days=days)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_mod_time < cutoff_date:
                os.remove(file_path)
                print(f"Deleted old image: {file_path}")

# Create a folder to save images
output_folder = "motion_images"
os.makedirs(output_folder, exist_ok=True)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Read the first frame to initialize background
ret, frame1 = cap.read()
if not ret:
    print("Failed to access webcam. Exiting...")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Convert the first frame to grayscale
gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray_frame1 = cv2.GaussianBlur(gray_frame1, (21, 21), 0)

print("Motion detector is running. Press 'q' to quit.")

while True:
    # Read the next frame
    ret, frame2 = cap.read()
    if not ret:
        break

    # Convert the current frame to grayscale
    gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray_frame2 = cv2.GaussianBlur(gray_frame2, (21, 21), 0)

    # Compute the absolute difference between the two frames
    frame_diff = cv2.absdiff(gray_frame1, gray_frame2)

    # Apply a threshold to the difference image
    _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

    # Find contours of the regions with motion
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Adjust the threshold area for sensitivity
            motion_detected = True
            # Draw a rectangle around the motion region
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if motion_detected:
        print("Motion detected! Sending email alert...")
        send_email_alert()

        # Capture images every second for 5 seconds
        for i in range(5):
            ret, image = cap.read()
            if ret:
                # Create a timestamped filename
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                image_path = os.path.join(output_folder, f"motion_{timestamp}_{i+1}.jpg")
                cv2.imwrite(image_path, image)
                print(f"Image saved: {image_path}")
            time.sleep(1)

        # Pause detection for 5 seconds
        time.sleep(5)

        # Delete old images
        delete_old_images(output_folder)

    # Display the current frame
    cv2.imshow("Motion Detector", frame2)

    # Update the background frame
    gray_frame1 = gray_frame2

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
