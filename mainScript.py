import os
import sys
import time
import cv2
import ultralytics
import pandas as pd
from ultralytics import YOLO
from tracker import *

class_list = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 
              'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

tracker=Tracker()
count=0

# Define the speed threshold
SPEED_THRESHOLD = 30  # speed in km/h

# Initialize YOLO model
model = YOLO("yolov8s.pt")

# Video input and output paths
for video in os.listdir(os.path.join('data','uploads')):
    cap = cv2.VideoCapture(os.path.join('data','uploads',video))
    # cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(os.path.join('public','output.avi'), fourcc, 20.0, (1020, 500))

if not os.path.exists(os.path.join('public','high_speed_frames')):
    os.makedirs(os.path.join('public','high_speed_frames'))

down = {}
up = {}
counter_down = []
counter_up = []

red_line_y = 198
blue_line_y = 268
offset = 6

count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    count += 1
    frame = cv2.resize(frame, (1020, 500))

    results = model.predict(frame)
    a = results[0].boxes.data
    a = a.detach().cpu().numpy()
    px = pd.DataFrame(a).astype("float")
    vehicle_list = []

    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        if 'car' in c:
            vehicle_list.append([x1, y1, x2, y2])
    bbox_id = tracker.update(vehicle_list)

    high_speed_detected = False

    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        cx = int((x3 + x4) / 2)
        cy = int((y3 + y4) / 2)

        if red_line_y < (cy + offset) and red_line_y > (cy - offset):
            down[id] = time.time()  # current time when vehicle touches the first line

        if id in down:
            if blue_line_y < (cy + offset) and blue_line_y > (cy - offset):
                elapsed_time = time.time() - down[id]  # time when vehicle touches the second line
                if counter_down.count(id) == 0:
                    counter_down.append(id)
                    distance = 10  # meters
                    speed_ms = distance / elapsed_time
                    speed_kh = speed_ms * 3.6  # km/h
                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)  # Draw bounding box
                    cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
                    cv2.putText(frame, str(int(speed_kh)) + 'Km/h', (x4, y4), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    if speed_kh > SPEED_THRESHOLD:
                        high_speed_detected = True

        if blue_line_y < (cy + offset) and blue_line_y > (cy - offset):
            up[id] = time.time()

        if id in up:
            if red_line_y < (cy + offset) and red_line_y > (cy - offset):
                elapsed1_time = time.time() - up[id]
                if counter_up.count(id) == 0:
                    counter_up.append(id)
                    distance1 = 10  # meters
                    speed_ms1 = distance1 / elapsed1_time
                    speed_kh1 = speed_ms1 * 3.6  # km/h
                    cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
                    cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)  # Draw bounding box
                    cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
                    cv2.putText(frame, str(int(speed_kh1)) + 'Km/h', (x4, y4), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                    if speed_kh1 > SPEED_THRESHOLD:
                        high_speed_detected = True

    text_color = (0, 0, 0)  # Black color for text
    yellow_color = (0, 255, 255)  # Yellow color for background
    red_color = (0, 0, 255)  # Red color for lines
    blue_color = (255, 0, 0)  # Blue color for lines

    cv2.rectangle(frame, (0, 0), (250, 90), yellow_color, -1)

    cv2.line(frame, (172, 198), (774, 198), red_color, 2)
    cv2.putText(frame, 'Red Line', (172, 198), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

    cv2.line(frame, (8, 268), (927, 268), blue_color, 2)
    cv2.putText(frame, 'Blue Line', (8, 268), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

    cv2.putText(frame, 'Going Down - ' + str(len(counter_down)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
    cv2.putText(frame, 'Going Up - ' + str(len(counter_up)), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

    # Save frame to the general detected frames folder
    # frame_filename = f'detected_frames/frame_{count}.jpg'
    # cv2.imwrite(frame_filename, frame)

    # Save frame to the high-speed folder if speed exceeds the threshold
    if high_speed_detected:
        high_speed_frame_filename = f'public/high_speed_frames/frame_{count}.jpg'
        cv2.imwrite(high_speed_frame_filename, frame)

    out.write(frame)

    cv2.imshow("frames", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
sys.exit(0)