# -*- coding: utf-8 -*-
"""
Original Deep Fashion Dataset has more than 5000 different classes, in very detail
This file just group them into several larger datasets

@author: liuming
"""

import os
import shutil
import csv
import time

data_path = '../data/'
label_file = 'list_bbox.txt'

Large_class = {}
selected_group = ['Dress','Tee','Blouse','Shorts','Tank','Skirt','Cardigan',
                  'Sweater','Jacket','Top','Blazer','Romper','Jeans','Jumpsuit',
                  'Leggings','Joggers','Hoodie','Sweatpants','Kimono','Coat',
                  'Cutoffs','Sweatshorts']

if os.path.exists(data_path + 'grouped'):
    shutil.rmtree(data_path + 'grouped')
os.mkdir(data_path + 'grouped')
for i in selected_group:
    if not os.path.exists(data_path + 'grouped/'+i):
        os.mkdir(data_path + 'grouped/' + i)
        
        
with open(os.path.join(data_path, label_file), 'r') as txtfile:
    label = csv.reader(txtfile, delimiter = ' ')
    for i, tmp in enumerate(label):
        if i<2: 
            continue
        
        tmp_large_class = tmp[0].split('/')[1].split('_')[-1]
        if tmp_large_class not in Large_class:
            Large_class[tmp_large_class] = 1
        else:
            Large_class[tmp_large_class] += 1
            
        if tmp_large_class in selected_group:
            new_name = tmp[0].split('/')[1] + '_' + tmp[0].split('/')[2]
            ori_file_path = data_path + tmp[0]
            new_file_path = data_path + 'grouped/' + tmp_large_class + '/' + new_name
            #print('copy from \n' + ori_file_path + '\n' +new_file_path + '\n')
            shutil.copy(ori_file_path, new_file_path)
        
        """
        category    total       keep    top_bottom
        
        Dress       72158       yes     all
        Tee         36887       yes     top
        Blouse      24557       yes     top
        Shorts      19666       yes     bottom
        Tank        15429       **
        Skirt       14773       yes     bottom
        Cardigan    13311       **
        Sweater     13123       no
        Jacket      10467       no
        Top         10078       **
        Blazer      7495        no
        Romper      7408        **
        Jeans       7076        yes     bottom
        Jumpsuit    6153        **
        Leggings    5013        **
        Joggers     4416        **
        Hoodie      4048        **
        Sweatpants  3048        **
        Kimono      2294        **
        Coat        2120        yes ?   all
        Cutoffs     1669        **
        Sweatshorts 1106        yes ?   bottom
        """
        
        