from ultralytics import YOLO
import cv2
import sys
import time
import os

FNAME = sys.argv[1]
print(FNAME)
cap = cv2.VideoCapture(FNAME)
fps = cap.get(cv2.CAP_PROP_FPS)
print("fps: ", fps)
frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print("frames: ", frames)
duration = int(frames / fps)
print("durations: ", duration)


def max2_idx(xi_1, x_1, xi_2, x_2):
    if x_1 > x_2:
        return xi_1
    return xi_2


def _getModel():
    d = sorted(os.listdir("models/cls"))
    model_path = 'models/cls/{}/best.pt'.format(d[-1])
    print("model_path: ", model_path)
    model = YOLO(model_path)
    return model


model = _getModel()
t = -1
frame_count = 0
written_frame_count = 0
while (True):
    t += 1
    ret, frame = cap.read()
    if ret == False:
        break
    if t % 10 == 0:
        print(t)
    results = model(frame, save=False, verbose=False, device=0)
    result = results[0]
    names = result.names
    data = result.probs.data
    c_idx = max2_idx(0, data[0].item(), 1, data[1].item())
    c = names[c_idx]
    if c == "top":
        cv2.imwrite(
            "./images/top/frame_{}.jpg".format(written_frame_count), frame)
        written_frame_count += 1
        frame_count += 1
    else:
        cv2.imwrite(
            "./images/not_top/frame_{}.jpg".format(written_frame_count), frame)
        written_frame_count += 1
        frame_count = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, fps * t)
