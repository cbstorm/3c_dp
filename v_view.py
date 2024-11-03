import cv2
from ultralytics import YOLO
import time
import sys
import os


def _getModel():
    d = sorted(os.listdir("models/od"))
    model_path = 'models/od/{}/best.pt'.format(d[-1])
    print("model_path: ", model_path)
    model = YOLO(model_path)
    return model


VID_PATH = sys.argv[1]
model = _getModel()
cap = cv2.VideoCapture(VID_PATH)

COLORS = dict()
COLORS["white"] = (255, 255, 255)
COLORS["yellow"] = (0, 255, 255)
COLORS["red"] = (255, 0, 0)

new_frame_time = 0
prev_frame_time = 0
while (True):
    ret, frame = cap.read()
    if ret == False:
        break
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    fps = "{:.2f}".format(fps)
    results = model.predict(frame, save=False, verbose=False, device=0)
    for idx, c in enumerate(results[0].boxes.cls):
        label = results[0].names[int(c)]
        xy = results[0].boxes.xyxy[int(idx)]
        xmin, ymin, xmax, ymax = int(xy[0]), int(xy[1]), int(xy[2]), int(xy[3])
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), COLORS[label], 1)

    cv2.putText(frame, fps, (8, 80), cv2.FONT_HERSHEY_SIMPLEX,
                2, (100, 255, 0), 4, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    prev_frame_time = new_frame_time
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
