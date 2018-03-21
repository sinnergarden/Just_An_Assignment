# -*- coding: utf-8 -*-
"""
create xml file for each image

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

def createXmlArray(img_path, img_shape, category, boundingbox_shape):
    
    folder = img_path.split('/')[-2]
    filename = img_path.split('/')[-1]
    path = img_path
    
    (height, width, depth) = img_shape
    (xmin, ymin, xmax, ymax) = boundingbox_shape
    
    array = {
            'folder': folder,
            'filename': filename,
            'path': path,
            'source': {'database':'deep fashion'},  
            
            'size':{'width': width,
                    'height': height,
                    'depth': depth
                    },
                
            'segmented': 0,       
            
            'object': {"name": category, 
                       "pose": "Unspecified",
                        "truncated": 0,
                        "difficult": 0,
                        "bndbox":{
                                   "xmin": xmin,
                                   "ymin": ymin,
                                   "xmax": xmax,
                                   "ymax": ymax
                                   }
                        }
            }
        
    
    return array

with open(os.path.join(root_path, label_file), 'r') as txtfile:
    label = csv.reader(txtfile, delimiter = ' ')
    for i, tmp in enumerate(label):
        if i<2: 
            continue
        tmp_large_class = tmp[0].split('/')[1].split('_')[-1]
        new_name = tmp[0].split('/')[1] + '_' + tmp[0].split('/')[2]
        new_file_path = data_path + tmp_large_class + '/' + new_name
        BBox[new_file_path] = tmp[-4:]

for folder in selected_group:
    for jpg_file in glob.glob(data_path + folder + '/*.jpg'): 
        
        if jpg_file.split('_')[-1] == 'border.jpg':
            continue
            
        """ calculate new names for txt files """
        Key = data_path + jpg_file.split('\\')[-1].split('_')[-3] \
                   +'/' + jpg_file.split('\\')[-1]
        
        image_file = data_path + folder + '/' \
                   + jpg_file.split('\\')[-1]
                   
        txt_file = data_path + folder + '/' \
                   + jpg_file.split('\\')[-1].split('.')[0]+'.txt'
                   
        xml_file = data_path + folder + '/' \
                   + jpg_file.split('\\')[-1].split('.')[0]+'.xml'         
        
        border_img = data_path + folder + '/' \
                   + jpg_file.split('\\')[-1].split('.')[0]+'_border.jpg'
                   
        border_txt = data_path + folder + '/' \
                   + jpg_file.split('\\')[-1].split('.')[0]+'_border.txt'
               
        border_xml = data_path + folder + '/' \
                   + jpg_file.split('\\')[-1].split('.')[0]+'_border.xml'
                   
        """ verify file names """
        #print(txt_file)        
        #print(image_file)
        #time.sleep(1)
        
        """ add border to original images """
        img = cv2.imread(image_file)        
        boundingbox = BBox[Key]
        (height, width, channel) = img.shape
        
        background = np.random.randint(255, size=(500,500,3), dtype=np.uint8)
        x_offset = int(random.random()*10000) % (499 - width)
        y_offset = int(random.random()*10000) % (499 - height)
        
        background[y_offset:y_offset+height, x_offset:x_offset+width] = img
        
        
        """ calculate normalized bounding box """
        bbox_x = int(boundingbox[0]) / width
        bbox_y = int(boundingbox[1]) / height
        bbox_w = (int(boundingbox[2]) - int(boundingbox[0]))/ width
        bbox_h = (int(boundingbox[3]) - int(boundingbox[1]))/ height
        boundingbox_shape = (int(boundingbox[0]),
                             int(boundingbox[1]),
                             int(boundingbox[2]),
                             int(boundingbox[3]))
        
        bbox_x_border = (int(boundingbox[0]) + x_offset) / 500
        bbox_y_border = (int(boundingbox[1]) + y_offset) / 500
        bbox_w_border = (int(boundingbox[2]) - int(boundingbox[0]))/ 500
        bbox_h_border = (int(boundingbox[3]) - int(boundingbox[1]))/ 500       
        boundingbox_shape_border = (int(boundingbox[0])+ x_offset,
                                    int(boundingbox[1])+ y_offset,
                                    int(boundingbox[2])+ x_offset,
                                    int(boundingbox[3])+ y_offset)        
        
        """ calculate normalized bounding box """
        array = createXmlArray(image_file, img.shape, folder, boundingbox_shape)
        xml = dicttoxml(array, custom_root='annotation', attr_type=False, root = True)
        
        array_border = createXmlArray(border_img, (500,500,3), folder, boundingbox_shape_border)
        xml_border = dicttoxml(array_border, custom_root='annotation', attr_type=False, root = True)
        
        """ write xml file """
        dom = parseString(xml)
        with open(xml_file,'w') as f:
            f.write(dom.toprettyxml())
        '''
        dom_border = parseString(xml_border)
        with open(border_xml,'w') as f:
            f.write(dom_border.toprettyxml())    
        '''
        """ save boundingbox file corresponding to original image and image after adding border """
        '''
        with open(txt_file,'w') as f:
            f.write(str(selected_group.index(folder)) + ' '
                    +str(bbox_x) + ' '
                    +str(bbox_y) + ' '
                    +str(bbox_w) + ' '
                    +str(bbox_h))
        
        with open(border_txt,'w') as f:
            f.write(str(selected_group.index(folder)) + ' '
                    +str(bbox_x_border) + ' '
                    +str(bbox_y_border) + ' '
                    +str(bbox_w_border) + ' '
                    +str(bbox_h_border))
        '''    
        #cv2.imwrite(border_img, background) 