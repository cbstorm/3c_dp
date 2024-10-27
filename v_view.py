import cv2
import sys

# print(sys.argv[1])
# cap = cv2.VideoCapture("srt://34.142.173.129:6000?streamid=/live/STR66FB56CF1?key=xExJSJGVcyBahJnQf7rlYwGhwiQ5m-")
cap = cv2.VideoCapture("https://hls0.wyrstream.nith-solutions.com/STR66F789564/playlist.m3u8")

# if (cap.isOpened()== False):
#     print("Error opening video file")


while(True):
    ret, frame = cap.read()
    if not ret:
        continue
    cv2.imshow('Frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    # if ret == True:
    # else:
    #     break

cap.release()
cv2.destroyAllWindows()