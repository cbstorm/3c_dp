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
vid = cv2.VideoCapture(VID_PATH)
fps = vid.get(cv2.CAP_PROP_FPS)
print("fps: ", fps)
frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
print("frames: ", frames)
duration = frames / fps
print("duration: ", duration)

FACTOR = 1


def check_moving(prev, curr):
    for k in curr:
        print("k: ", k, "prevk: ", prev.get(k))
    return False


def main():
    t = -1
    model = _getModel()
    prev = dict()
    while True:
        t += 1
        ret, frame = vid.read()
        if not ret:
            break
        vid.set(cv2.CAP_PROP_POS_FRAMES, fps * t * FACTOR)
        results = model.predict(frame, save=False, verbose=False, device=0)
        curr = dict()
        for idx, c in enumerate(results[0].boxes.cls):
            label = results[0].names[int(c)]
            xy = results[0].boxes.xyxy[int(idx)]
            xmin, ymin, xmax, ymax = int(xy[0]), int(
                xy[1]), int(xy[2]), int(xy[3])
            curr[label] = (xmin, ymin, xmax, ymax)
        if t == 0:
            prev = curr
            continue
        is_moving = check_moving(prev, curr)
        prev = curr
        print("is_moving: ", is_moving)
        print("-------")


if __name__ == '__main__':
    main()
