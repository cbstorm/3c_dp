import cv2
import sys

timestamp = sys.argv[2]
FNAME = sys.argv[1]

vid = cv2.VideoCapture(FNAME)
fps = vid.get(cv2.CAP_PROP_FPS)

vid.set(cv2.CAP_PROP_POS_FRAMES, int(fps) * int(timestamp))

ret, frame = vid.read()
cv2.imwrite("tmp/frame_0.png", frame)
