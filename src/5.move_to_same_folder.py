# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 11:50:08 2018

@author: liuming
"""

import os
import shutil
import csv
import glob
import cv2
import time
import random
import numpy as np
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

root_path = '../data/'
data_path = '../data/validation/'
label_file = 'list_bbox.txt'
selected_group = os.listdir(data_path)
BBox = {}

for folder in selected_group:
    for file in glob.glob(data_path + folder + '/*'): 
        new_file = data_path + file.split('\\')[-1]
        shutil.move(file, new_file)
    os.rmdir(data_path + folder)