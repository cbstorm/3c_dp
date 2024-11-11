import os
import cv2
import sys

VID_PATH = sys.argv[1]
WINDOW_NAME = os.path.basename(VID_PATH)
vid = cv2.VideoCapture(VID_PATH)
fps = vid.get(cv2.CAP_PROP_FPS)
frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
duration = frames / fps
print("fps: ", fps, " frames: ", frames, " duration: ", duration, "s")
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW_NAME, 1280, 720)
while True:
    ret, frame = vid.read()
    if not ret:
        break
    cv2.imshow(WINDOW_NAME, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


vid.release()
cv2.destroyAllWindows()
