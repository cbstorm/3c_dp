import os
import cv2
from ultralytics import YOLO


def _getModel():
    d = sorted(os.listdir("models/od"))
    model_path = 'models/od/{}/best.pt'.format(d[-1])
    print("model_path: ", model_path)
    model = YOLO(model_path)
    return model


def main():
    model = _getModel()
    files = os.listdir("images")
    for i, m in enumerate(files):
        img = cv2.imread("images/{}".format(m))
        result = model.predict(img, save=False, verbose=False, device=0)[0]
        zipped = list(zip(result.boxes.cls, result.boxes.data))
        sorted_zipped = sorted(zipped, key=lambda x: x[0])
        classes, boxes_data = zip(*sorted_zipped)
        min_score = 1
        for idx, c in enumerate(classes):
            cls_name = result.names[int(c)]
            xmin, ymin, xmax, ymax, score, cls_idx = boxes_data[idx]
            xmin, ymin, xmax, ymax, score = xmin.item(
            ), ymin.item(), xmax.item(), ymax.item(), score.item()
            min_score = min(min_score, score)

        if min_score < 0.9:
            print(min_score)
        else:
            os.system('rm -rf images/{}'.format(m))

        # if i % 2 != 0:


if __name__ == '__main__':
    main()
