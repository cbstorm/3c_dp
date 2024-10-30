from ultralytics import YOLO
import os
import shutil
import random
os.environ['WANDB_DISABLED'] = 'true'

TRAIN_RATE = 80
TEST_RATE = 10
VAL_RATE = 10

RAW_DATASET_DIR = "__classify_dataset"
TOP_DIR = "{}/top".format(RAW_DATASET_DIR)
NOT_TOP_DIR = "{}/not_top".format(RAW_DATASET_DIR)
DATASET_DIR = "dataset"
TRAIN_DIR = "{}/train".format(DATASET_DIR)
TOP_TRAIN_DIR = "{}/top".format(TRAIN_DIR)
NOT_TOP_TRAIN_DIR = "{}/not_top".format(TRAIN_DIR)
TEST_DIR = "{}/test".format(DATASET_DIR)
TOP_TEST_DIR = "{}/top".format(TEST_DIR)
NOT_TOP_TEST_DIR = "{}/not_top".format(TEST_DIR)
VAL_DIR = "{}/val".format(DATASET_DIR)
TOP_VAL_DIR = "{}/top".format(VAL_DIR)
NOT_TOP_VAL_DIR = "{}/not_top".format(VAL_DIR)

os.makedirs(DATASET_DIR)
os.makedirs(TRAIN_DIR)
os.makedirs(TOP_TRAIN_DIR)
os.makedirs(NOT_TOP_TRAIN_DIR)
os.makedirs(TEST_DIR)
os.makedirs(TOP_TEST_DIR)
os.makedirs(NOT_TOP_TEST_DIR)
os.makedirs(VAL_DIR)
os.makedirs(TOP_VAL_DIR)
os.makedirs(NOT_TOP_VAL_DIR)

TOP_IMAGES = os.listdir(TOP_DIR)
random.shuffle(TOP_IMAGES)
NOT_TOP_IMAGES = os.listdir(NOT_TOP_DIR)
random.shuffle(NOT_TOP_IMAGES)


TOP_TRAIN_RANGE = (0, int(len(TOP_IMAGES) / 100 * TRAIN_RATE))
NOT_TOP_TRAIN_RANGE = (0, int(len(NOT_TOP_IMAGES) / 100 * TRAIN_RATE))

TOP_TEST_RANGE = (
    TOP_TRAIN_RANGE[1], TOP_TRAIN_RANGE[1] + int(len(TOP_IMAGES) / 100 * TEST_RATE))
NOT_TOP_TEST_RANGE = (
    NOT_TOP_TRAIN_RANGE[1], NOT_TOP_TRAIN_RANGE[1] + int(len(NOT_TOP_IMAGES) / 100 * TEST_RATE))

TOP_VAL_RANGE = (
    TOP_TEST_RANGE[1], len(TOP_IMAGES))
NOT_TOP_VAL_RANGE = (
    NOT_TOP_TEST_RANGE[1], len(NOT_TOP_IMAGES))

print(TOP_TRAIN_RANGE, NOT_TOP_TRAIN_RANGE)
print(TOP_TEST_RANGE, NOT_TOP_TEST_RANGE)
print(TOP_VAL_RANGE, NOT_TOP_VAL_RANGE)

# Train data
for i in range(TOP_TRAIN_RANGE[0], TOP_TRAIN_RANGE[1]):
    shutil.copy("{}/{}".format(TOP_DIR, TOP_IMAGES[i]),
                "{}/{}".format(TOP_TRAIN_DIR, TOP_IMAGES[i]))

print("Copy data top train done")

for i in range(NOT_TOP_TRAIN_RANGE[0], NOT_TOP_TRAIN_RANGE[1]):
    shutil.copy("{}/{}".format(NOT_TOP_DIR, NOT_TOP_IMAGES[i]),
                "{}/{}".format(NOT_TOP_TRAIN_DIR, NOT_TOP_IMAGES[i]))

print("Copy data not_top train done")

# Test data
for i in range(TOP_TEST_RANGE[0], TOP_TEST_RANGE[1]):
    shutil.copy("{}/{}".format(TOP_DIR, TOP_IMAGES[i]),
                "{}/{}".format(TOP_TEST_DIR, TOP_IMAGES[i]))

print("Copy data top test done")

for i in range(NOT_TOP_TEST_RANGE[0], NOT_TOP_TEST_RANGE[1]):
    shutil.copy("{}/{}".format(NOT_TOP_DIR, NOT_TOP_IMAGES[i]),
                "{}/{}".format(NOT_TOP_TEST_DIR, NOT_TOP_IMAGES[i]))

print("Copy data not_top test done")


# Val data
for i in range(TOP_VAL_RANGE[0], TOP_VAL_RANGE[1]):
    shutil.copy("{}/{}".format(TOP_DIR, TOP_IMAGES[i]),
                "{}/{}".format(TOP_VAL_DIR, TOP_IMAGES[i]))

print("Copy data top valid done")

for i in range(NOT_TOP_VAL_RANGE[0], NOT_TOP_VAL_RANGE[1]):
    shutil.copy("{}/{}".format(NOT_TOP_DIR, NOT_TOP_IMAGES[i]),
                "{}/{}".format(NOT_TOP_VAL_DIR, NOT_TOP_IMAGES[i]))

print("Copy data not_top valid done")

# Load model
model = YOLO("yolov8n-cls.pt")

# Train the model
results = model.train(data=DATASET_DIR, epochs=100, device=0)
