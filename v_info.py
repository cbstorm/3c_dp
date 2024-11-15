import os
import sys
import cv2

VID_PATH = sys.argv[1]
vid = cv2.VideoCapture(VID_PATH)
fps = vid.get(cv2.CAP_PROP_FPS)
frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
duration_h = int(frames / fps / 3600)
duration_m = int((int(frames / fps) % 3600) / 60)
duration_s = int(frames / fps) - (duration_h * 3600) - (duration_m * 60)
print("fps: ", fps,  "frames: ", frames, "width: ", width, "height: ",
      height, "durations: {}h{}m{}s".format(duration_h, duration_m, duration_s))
