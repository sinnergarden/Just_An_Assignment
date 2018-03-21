# -*- coding: utf-8 -*-
"""
This file mainly adds random border to those images

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
        
        if jpg_file.split('_')[-1] == 'border.jpg':
            continue
            
        """ calculate new names for txt files """
        image_file = data_path + 'grouped/' + folder + '/' \
                   + jpg_file.split('\\')[-1]
                   
        txt_file = data_path + 'grouped/' + folder + '/' \
                   + jpg_file.split('\\')[-1].split('.')[0]+'.txt'
        
        border_img = data_path + 'grouped/' + folder + '/' \
                   + jpg_file.split('\\')[-1].split('.')[0]+'_border.jpg'
                   
        border_txt = data_path + 'grouped/' + folder + '/' \
                   + jpg_file.split('\\')[-1].split('.')[0]+'_border.txt'
                   
                   
        """ verify file names """
        #print(txt_file)        
        #print(image_file)
        #time.sleep(1)
        
        """ add border to original images """
        img = cv2.imread(image_file)        
        boundingbox = BBox[image_file]
        (height, width, channel) = img.shape
        
        background = np.zeros((500,500,3), dtype=np.uint8)
        x_offset = int(random.random()*10000) % (499 - width)
        y_offset = int(random.random()*10000) % (499 - height)
        
        background[y_offset:y_offset+height, x_offset:x_offset+width] = img
               
        
        """ verify bounding box """
        """
        #.rectangle(background, 
        #              (int(boundingbox[0])+x_offset,int(boundingbox[1])+y_offset),
        #              (int(boundingbox[2])+x_offset,int(boundingbox[3])+y_offset),
        #              (0,255,0), 3)
        #cv2.imshow('', background)
        #cv2.waitKey(0)
        """
        
        """ calculate normalized bounding box """
        bbox_x = int(boundingbox[0]) / width
        bbox_y = int(boundingbox[1]) / height
        bbox_w = (int(boundingbox[2]) - int(boundingbox[0]))/ width
        bbox_h = (int(boundingbox[3]) - int(boundingbox[1]))/ height

        bbox_x_border = (int(boundingbox[0]) + x_offset) / 500
        bbox_y_border = (int(boundingbox[1]) + y_offset) / 500
        bbox_w_border = (int(boundingbox[2]) - int(boundingbox[0]))/ 500
        bbox_h_border = (int(boundingbox[3]) - int(boundingbox[1]))/ 500        
        
        category = 1
        
        """ verify normolized bbox """
        """
        cv2.rectangle(img, (int(bbox_x * width), 
                            int(bbox_y * height)),
                           (int((bbox_x + bbox_w) * width),
                            int((bbox_y + bbox_h) * height)),
                            (0,255,0), 3)
        cv2.imshow('ori_img', img)
        
        cv2.rectangle(background, (int(bbox_x_border * width), 
                                   int(bbox_y_border * height)),
                                   (int((bbox_x_border + bbox_w_border) * width),
                                   int((bbox_y_border + bbox_h_border) * height)),
                                   (0,255,0), 3)
        cv2.imshow('border', background)
        cv2.waitKey(0)
        """
        
        """ save boundingbox file corresponding to original image and image after adding border """
        
        with open(txt_file,'w') as f:
            f.write(str(category) + ' '
                    +str(bbox_x) + ' '
                    +str(bbox_y) + ' '
                    +str(bbox_w) + ' '
                    +str(bbox_h))
        
        with open(border_txt,'w') as f:
            f.write(str(category) + ' '
                    +str(bbox_x_border) + ' '
                    +str(bbox_y_border) + ' '
                    +str(bbox_w_border) + ' '
                    +str(bbox_h_border))
            
        cv2.imwrite(border_img, background) 