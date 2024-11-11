import os
import cv2
import sys

VID_PATH = sys.argv[1]
VID_NAME = os.path.splitext(os.path.basename(VID_PATH))[0]
vid = cv2.VideoCapture(VID_PATH)
fps = vid.get(cv2.CAP_PROP_FPS)
frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
x, y = 520, 970
w, h = 1920 - x, 1030 - y

width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

size = (width, height)
writer = cv2.VideoWriter('videos/{}_hidden_banner.mp4'.format(VID_NAME),
                         cv2.VideoWriter_fourcc(*'MP4V'),
                         fps, size)
n = 0
while True:
    n += 1
    ret, frame = vid.read()
    if not ret:
        break
    # ROI = frame[y:y+h, x:x+w]
    # blur = cv2.GaussianBlur(ROI, (51, 51), 0)
    # frame[y:y+h, x:x+w] = blur
    cv2.rectangle(frame, (x, y), (1920, 1030), (0, 0, 0), -1)
    writer.write(frame)
    if n % 100 == 0:
        print(n, "/", frames)
