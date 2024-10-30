from ultralytics import YOLO
import cv2
import sys

FNAME = sys.argv[1]
cap = cv2.VideoCapture(FNAME)


def _getModel():
    d = os.listdir("models/cls")
    model_path = 'models/cls/{}/best.pt'.format(d[0])
    print("model_path: ", model_path)
    model = YOLO(model_path)
    return model


def _view():
    model = _getModel()
    while (True):
        ret, frame = cap.read()
        if ret == False:
            break
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        fps = "{:.2f}".format(fps)
        results = model(frame, save=False, verbose=False, device=0)
        print(results)


def main():
    _view()
    return 0


if __name__ == '__main__':
    main()
