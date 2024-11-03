import os
import cv2
from ultralytics import YOLO
import sys
import re
from lib.file import SortedAlphanumeric


FNAME = sys.argv[1]
vid = cv2.VideoCapture(FNAME)
fps = vid.get(cv2.CAP_PROP_FPS)
print("fps: ", fps)
frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
print("frames: ", frames)
duration = int(frames / fps)
print("durations: ", duration)


def merge():
    os.system(
        "ffmpeg -f concat -safe 0 -i ./tmp/vid_list.txt -c copy ./videos/vid_concat.mp4")


def generate_vid_list_file():
    dir = "./tmp/vid_0"
    files = SortedAlphanumeric(os.listdir(dir))
    with open("./tmp/vid_list.txt", "a") as f:
        for fi in files:
            f.write("file '{}'\n".format("./vid_0/{}".format(fi)))


def segment_video(time_ranges):
    padding = 3
    threshold = 12
    for i, r in enumerate(time_ranges):
        if i % 2 != 0:
            continue
        if len(r) < 2:
            r += [duration]
        if r[1] - r[0] <= threshold:
            continue
        if r[0] > padding:
            r[0] = r[0] - padding
        r[1] = r[1] + padding
        os.system("ffmpeg -ss {FROM} -to {TO} -i {FNAME} -map 0 -c copy ./tmp/vid_0/{VNAME}_{FROM}_{TO}.mp4".format(
            FROM=format(r[0], '.1f'), TO=format(r[1], '.1f'), FNAME=FNAME, VNAME=os.path.splitext(os.path.basename(FNAME))[0]))


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


def main():
    model = _getModel()
    t = -1
    factor = 1
    time_range = []
    is_on_top = 0
    diff = 0
    while (True):
        t += 1
        if t % 10 == 0:
            print(t)
        ret, frame = vid.read()
        if ret == False:
            break
        vid.set(cv2.CAP_PROP_POS_FRAMES, fps * t * factor)
        result = model(frame, save=False, verbose=False, device=0)[0]
        names = result.names
        data = result.probs.data
        c_idx = max2_idx(0, data[0].item(), 1, data[1].item())
        c = names[c_idx]
        if c == "top":
            if is_on_top == 0:
                diff = 1
            is_on_top = 1
        else:
            if is_on_top == 1:
                diff = 1
            is_on_top = 0

        if diff == 1:
            if len(time_range) != 0 and len(time_range[-1]) == 1:
                time_range[-1] += [t * factor]
                print("{}/{}\n-------".format(t * factor, duration))
            time_range += [[t * factor]]
            print(t * factor)
        diff = 0

    segment_video(time_range)
    generate_vid_list_file()
    merge()


if __name__ == '__main__':
    main()
