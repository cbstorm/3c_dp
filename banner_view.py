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

COLORS = dict()
COLORS["white"] = (255, 255, 255)
COLORS["yellow"] = (0, 255, 255)
COLORS["red"] = (255, 0, 0)

new_frame_time = 0
prev_frame_time = 0
WINDOW_NAME = os.path.basename(VID_PATH)
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW_NAME, 1280, 720)
while (True):
    ret, frame = cap.read()
    if ret == False:
        break
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    fps = "{:.2f}".format(fps)
    result = model.predict(frame, save=False, verbose=False, device=0)[0]
    boxes = result.boxes.data
    for b in boxes:
        xmin, ymin, xmax, ymax, score = int(b[0]), int(
            b[1]), int(b[2]), int(b[3]), int(b[4] * 100)
        if score < 90:
            continue
        # ROI = frame[ymin:ymin+ymax, xmin:xmin+xmax]
        # blur = cv2.GaussianBlur(ROI, (51, 51), 0)
        # frame[ymin:ymin+ymax, xmin:xmin+xmax] = blur
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 255, 255), 2)
    cv2.imshow(WINDOW_NAME, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
