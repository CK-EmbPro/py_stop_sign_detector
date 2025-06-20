import cv2
import serial
import time

# Load Haar cascade for stop sign detection
stop_cascade = cv2.CascadeClassifier("haarcascade_stop.xml")

# Initialize serial communication
# ser = serial.Serial('COM3', 9600)

# Initialize video capture (0 = default camera)
cap = cv2.VideoCapture(0)

# Control variables
last_stop_time = 0
stop_duration = 3  # seconds
sending_stop = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    stops = stop_cascade.detectMultiScale(gray, 1.3, 5)

    if len(stops) > 0:
        if not sending_stop:
            print("Stop sign detected! Sending '1'")
            # ser.write(b'1')
            last_stop_time = time.time()
            sending_stop = True
    else:
        if sending_stop and time.time() - last_stop_time >= stop_duration:
            print("Resume movement. Sending '0'")
            # ser.write(b'0')
            sending_stop = False
        # elif not sending_stop:
        #     ser.write(b'0')

    # Draw rectangles for visualization
    for (x, y, w, h) in stops:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    cv2.imshow('Stop Sign Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
# ser.close()
