# -*- coding: utf-8 -*-
"""
This file mainly prepare yolo training txt for every picture
we give the same name to those txt file corresponding to each image.

@author: liuming
"""

import os
import shutil
import csv
import glob
import cv2
import time

data_path = '../data/'
label_file = 'list_bbox.txt'

BBox = {}

'''
selected_group = ['Dress','Tee','Blouse','Shorts','Tank','Skirt','Cardigan',
                  'Sweater','Jacket','Top','Blazer','Romper','Jeans','Jumpsuit',
                  'Leggings','Joggers','Hoodie','Sweatpants','Kimono','Coat',
                  'Cutoffs','Sweatshorts']
'''

selected_group = ['Sweatshorts']

with open(os.path.join(data_path, label_file), 'r') as txtfile:
    label = csv.reader(txtfile, delimiter = ' ')
    for i, tmp in enumerate(label):
        if i<2: 
            continue
        tmp_large_class = tmp[0].split('/')[1].split('_')[-1]
        new_name = tmp[0].split('/')[1] + '_' + tmp[0].split('/')[2]
        new_file_path = data_path + 'grouped/' + tmp_large_class + '/' + new_name
        BBox[new_file_path] = tmp[-4:]

for folder in selected_group:
    for jpg_file in glob.glob(data_path + 'grouped/' + folder + '/*.jpg'):
        
        image_file = data_path + 'grouped/' + folder + '/' \
                   + jpg_file.split('\\')[-1]
        txt_file = data_path + 'grouped/' + folder + '/' \
                   + jpg_file.split('\\')[-1].split('.')[0]+'.txt'
        
        """ verify file names """
        #print(txt_file)        
        #print(image_file)
        #time.sleep(1)
        img = cv2.imread(image_file)        
        boundingbox = BBox[image_file]
        
        """ verify bounding box """
        #cv2.rectangle(img, 
        #              (int(boundingbox[0]),int(boundingbox[1])),
        #              (int(boundingbox[2]),int(boundingbox[3])),
        #              (0,255,0), 3)
        #cv2.imshow('', img)
        #cv2.waitKey(0)
        
        (height, width, channel) = img.shape
        bbox_x = int(boundingbox[0]) / width
        bbox_y = int(boundingbox[1]) / height
        bbox_w = (int(boundingbox[2]) - int(boundingbox[0]))/ width
        bbox_h = (int(boundingbox[3]) - int(boundingbox[1]))/ height
        category = 1
        
        """ verify normolized bbox """
        #cv2.rectangle(img, (int(bbox_x * width), 
        #                    int(bbox_y * height)),
        #                   (int((bbox_x + bbox_w) * width),
        #                    int((bbox_y + bbox_h) * height)),
        #                    (0,255,0), 3)
        #cv2.imshow('', img)
        #cv2.waitKey(0)
        
        with open(txt_file,'w') as f:
            f.write(str(category) + ' '
                    +str(bbox_x) + ' '
                    +str(bbox_y) + ' '
                    +str(bbox_w) + ' '
                    +str(bbox_h))





























