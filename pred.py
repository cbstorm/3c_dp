import os
import cv2
from ultralytics import YOLO
import time
from lib import lstasks, file, lbstudio


def _getModel():
    d = os.listdir("models/od")
    model_path = 'models/od/{}/best.pt'.format(d[0])
    print("model_path: ", model_path)
    model = YOLO(model_path)
    return model


def Pred():
    model = _getModel()
    tasks = lstasks.GetListNewTasks()
    for i, t in enumerate(tasks):
        print(i, t["id"])
        f_name = os.path.basename(t["image"])
        file.HttpDownload(f_name=f_name)
        img_path = 'tmp/{img}'.format(img=f_name)
        img = cv2.imread(img_path)
        result = model.predict(img, save=False, verbose=False, device=0)[0]
        origin_h, origin_w = result.orig_shape
        pred_objs = []
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
            pred_obj = {
                "original_width": origin_w,
                "original_height": origin_h,
                "image_rotation": 0,
                "from_name": "label",
                "to_name": "image",
                "type": "rectanglelabels",
                "value": {
                    "x": xmin / origin_w * 100,
                    "y": ymin / origin_h * 100,
                    "width": (xmax - xmin) / origin_w * 100,
                    "height": (ymax - ymin) / origin_h * 100,
                    "rotation": 0,
                    "values": {"rectanglelabels": [
                        cls_name
                    ]},
                },
            }
            pred_objs += [pred_obj]

        lbstudio.client.predictions.create(task=t["id"],
                                           result=pred_objs, score=min_score,  model_version="yolo-v8")
        os.remove(img_path)


def main():
    Pred()


if __name__ == '__main__':
    main()
