from ultralytics import YOLO
import cv2
import sys
import time
import os

FNAME = sys.argv[1]
print(FNAME)
cap = cv2.VideoCapture(FNAME)


def max2_idx(xi_1, x_1, xi_2, x_2):
    if x_1 > x_2:
        return xi_1
    return xi_2


def _getModel():
    d = os.listdir("models/cls")
    model_path = 'models/cls/{}/best.pt'.format(d[0])
    print("model_path: ", model_path)
    model = YOLO(model_path)
    return model


model = _getModel()
total_frame = 0
frame_count = 0
written_frame_count = 0
while (True):
    ret, frame = cap.read()
    if ret == False:
        break
    total_frame += 1
    if total_frame % 1000 == 0:
        print(total_frame)
    results = model(frame, save=False, verbose=False, device=0)
    result = results[0]
    names = result.names
    data = result.probs.data
    c_idx = max2_idx(0, data[0].item(), 1, data[1].item())
    c = names[c_idx]
    if c == "top":
        if frame_count % 20 == 0:
            cv2.imwrite(
                "./images/frame_{}.jpg".format(written_frame_count), frame)
            written_frame_count += 1

        frame_count += 1
        # cv2.putText(frame, "TOP", (8, 80), cv2.FONT_HERSHEY_SIMPLEX,
        #             2, (100, 255, 0), 4, cv2.LINE_AA)
    else:
        frame_count = 0
    # cv2.imshow("frame", frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# cap.release()
# cv2.destroyAllWindows()
