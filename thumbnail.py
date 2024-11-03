import cv2


vid = cv2.VideoCapture("videos/vid_concat.mp4")

while True:
    ret, frame = vid.read()
    cv2.imwrite("tmp/frame_0.png", frame)
    break
