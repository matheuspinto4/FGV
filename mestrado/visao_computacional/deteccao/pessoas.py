import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# -- Loading the video
videoPath = "security_footage.mp4"

# -- loading the model
model = YOLO('yolov8n.pt')


frame_number = 0
capture = cv2.VideoCapture(videoPath)
track_history = defaultdict(lambda: []) 

while(capture.isOpened()):
    frame_number += 1
    ret, frame = capture.read()
    if ret == False:
        break

    frame = cv2.resize(src=frame, dsize=None, fx=0.8, fy=0.8)
    results = model.track(frame, persist=True, classes=0)

    if results[0].boxes.id is not None:
        boxes = results[0].boxes.xywh.cpu()
        track_ids = results[0].boxes.id.int().cpu().tolist()    

        for box, track_id in zip(boxes, track_ids):
            x, y, w, h = box

            center_x = int(x)          
            center_y = int(y)  

            track = track_history[track_id]
            track.append((center_x, center_y))

            if len(track) > 30:
                track.pop(0)

            cv2.circle(frame, (center_x, center_y), 5, (0,0,255), -1)
            points = np.hstack(track).astype(np.int32).reshape((-1,1,2))
            cv2.polylines(frame, [points], isClosed=False, color=(0,255,0), thickness=2)   

    cv2.imshow("Rastro de clientes", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()