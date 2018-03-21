# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 13:58:27 2018

@author: liuming
"""

from darkflow.net.build import TFNet
import cv2
import numpy as np


options = {"model": "cfg/yolo-fashion.cfg", 
           "load": -1, #or 9062,
           "threshold": 0.1, 'gpu':1.0}

tfnet = TFNet(options)
cap = cv2.VideoCapture(0)
mark = 100
x = 1

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Display the resulting frame
    
    if x == ord('d') and mark <= 440:
        mark += 10
    if x == ord('a') and mark >= 60:
        mark -= 10
    if x == 27:
        break
    threshold = 0.00225 * (mark-50) + 0.1
    
    
    result = tfnet.return_predict(RGB)
    
    for detection in result:
        label = detection['label']
        confidence = format(float(detection['confidence']), '.2f')
        tl = (int(detection['topleft']['x']),
              int(detection['topleft']['y']))
        br = (int(detection['bottomright']['x']),
              int(detection['bottomright']['y']))
        
        if float(confidence) >= threshold:
            cv2.rectangle(frame,tl,br,(0,255,0),3)
            
            cv2.putText(frame, label + ' ' + confidence, tl, 
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1,(255,255,255),1,cv2.LINE_AA)

    cv2.imshow('frame', frame)
    
    background = np.ones((500,500,3), dtype = np.uint8) * 255
    cv2.putText(background, '0.1', (50,250),  cv2.FONT_HERSHEY_COMPLEX_SMALL,
                1,(0,0,0),1,cv2.LINE_AA)
    cv2.putText(background, '1.0', (450,250),  cv2.FONT_HERSHEY_COMPLEX_SMALL,
                1,(0,0,0),1,cv2.LINE_AA)
    cv2.line(background, (50, 250), (450, 250), (0,0,0), 3)
    cv2.circle(background,(mark, 250), 8, (255,0,0), 3)
    
    cv2.putText(background, 'current value: '+ format(threshold, '.2f'), (150,100),  
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                1,(0,0,0),1,cv2.LINE_AA)   
    
    cv2.imshow('threshold_setting', background)
    x = cv2.waitKey(30)
    
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
