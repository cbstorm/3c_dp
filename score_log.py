import cv2
import sys
import easyocr
import os

VID_PATH = sys.argv[1]
FACTOR = sys.argv[2]
vid = cv2.VideoCapture(VID_PATH)
fps = vid.get(cv2.CAP_PROP_FPS)
frame = vid.get(cv2.CAP_PROP_FRAME_COUNT)
duration = vid.get(cv2.CAP_PROP_FRAME_COUNT)
t = 0
reader = easyocr.Reader(['en'])
while True:
    t += 1
    ret, frame = vid.read()
    if not ret:
        break
    vid.set(cv2.CAP_PROP_POS_FRAMES, fps * t * float(FACTOR))
    # tmp_path = "tmp/{}.jpg".format("score_tmp")
    # cv2.imwrite(tmp_path, frame)
    result = reader.readtext(frame, detail=0)
    print("t=", t, result)
# import easyocr
# reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
# result = reader.readtext('chinese.jpg')
