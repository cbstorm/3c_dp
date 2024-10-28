from ultralytics import YOLO
import os
import shutil
os.environ['WANDB_DISABLED'] = 'true'


DATASET_RAW_DIR = '__dataset'
CONFIG_FILE = '3c.yaml'
DATASET = "datasets/dataset"
images_train = "{dataset}/images/train".format(dataset=DATASET)
images_val = "{dataset}/images/val".format(dataset=DATASET)
labels_train = "{dataset}/labels/train".format(dataset=DATASET)
labels_val = "{dataset}/labels/val".format(dataset=DATASET)
os.makedirs(DATASET)
os.makedirs(images_train)
os.makedirs(images_val)
os.makedirs(labels_train)
os.makedirs(labels_val)

images_path = os.listdir(DATASET_RAW_DIR + "/images")
n_train = int(len(images_path) * 80 / 100)
picked_img_train_list = images_path[:n_train]
picked_img_val_list = images_path[n_train:]
for f in picked_img_train_list:
    image_source = DATASET_RAW_DIR + "/images" + "/" + f
    image_dest = images_train + "/" + f
    f_name, _ = os.path.splitext(f)
    label_source = DATASET_RAW_DIR + "/labels" + "/" + f_name + ".txt"
    label_dest = labels_train + "/" + f_name + ".txt"
    shutil.copyfile(image_source, image_dest)
    shutil.copyfile(label_source, label_dest)

for f in picked_img_val_list:
    image_source = DATASET_RAW_DIR + "/images" + "/" + f
    image_dest = images_val + "/" + f
    f_name, _ = os.path.splitext(f)
    label_source = DATASET_RAW_DIR + "/labels" + "/" + f_name + ".txt"
    label_dest = labels_val + "/" + f_name + ".txt"
    shutil.copyfile(image_source, image_dest)
    shutil.copyfile(label_source, label_dest)

with open(CONFIG_FILE, "w") as f:
    f.write('''path: {ds} # dataset root dir
train: images/train # train images (relative to 'path') 4 images
val: images/val # val images (relative to 'path') 4 images

# Classes
names:
  0: red
  1: white
  2: yellow
'''.format(ds='dataset'))

model = YOLO("yolov8n.pt")
results = model.train(data=CONFIG_FILE, epochs=120, device=0)
