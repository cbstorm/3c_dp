import cv2
from ultralytics import YOLO
import time
import sys
import os


def _getModel():
    d = sorted(os.listdir("models/banner"))
    model_path = 'models/banner/{}/best.pt'.format(d[-1])
    print("model_path: ", model_path)
    model = YOLO(model_path)
    return model


VID_PATH = sys.argv[1]
model = _getModel()
cap = cv2.VideoCapture(VID_PATH)

new_frame_time = 0
prev_frame_time = 0
while (True):
    ret, frame = cap.read()
    if ret == False:
        break
    new_frame_time = time.time()
    result = model.predict(frame, save=False, verbose=False, device=0)[0]
    boxes = result.boxes.xywh
    for b in boxes:
        x, y, w, h = int(b[0]), int(b[1]), int(b[2]), int(b[3])
        ROI = frame[y:y+h, x:x+w]
        blur = cv2.GaussianBlur(ROI, (51, 51), 0)
        frame[y:y+h, x:x+w] = blur
