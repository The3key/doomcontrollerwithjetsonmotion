import os
from os import listdir

#pulling train png names from asl_original/train
#and spits them into train.txt

folder_dir = "/home/nvidia/jetson-inference/python/training/detection/ssd/img"

for images in os.listdir(folder_dir):
    if images.endswith(".jpg"):
            image_print = images[:-4]
            with open('/home/nvidia/jetson-inference/python/training/detection/ssd/datamain.txt', 'a') as train:
                train.write(image_print)
                train.write('\n')
