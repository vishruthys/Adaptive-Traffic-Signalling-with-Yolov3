#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
#       Description about this file here
#       Developers : Venkat Sai Krishna,
#                   Vishruth Y S, 
#                   Sujay Biradar
# =============================================================================
#       Copyright (C) 2019  *Developers* 
# 
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
# 
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
# 
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <https://www.gnu.org/licenses/>.
# =============================================================================

# =============================================================================
#       Removing the above copyright notice from the code is a direct breach 
#       of GNU's GPL v3.0 . If you have modified this code or developed 
#       any feature, feel free to append your name to the copyright name list.
#
#       This code is part of the repo owned by https://github.com/vishruthys/
# =============================================================================




import cv2
import matplotlib.pyplot as plt
import numpy as np

def getOutputsNames(net):
    layersNames = net.getLayerNames()
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Darw a rectangle surrounding the object and its class name
def draw_pred(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 5)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)



#Load names classes
options = {"config": "./yolov3.cfg",
           "weights": "/home/vishruthys/Projects/yolov3.weights",
           "classes": "./coco.names",
           }

classes = None
with open(options["classes"], 'r') as f:
    classes = [line.strip() for line in f.readlines()]

#Generate color for each class randomly
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

#Define network from configuration file and load the weights from the given weights file
net = cv2.dnn.readNet(options["weights"],options["config"])
    
def detection(image, video_index):

    blob = cv2.dnn.blobFromImage(image, 1.0/255.0, (416,416), [0,0,0], True, crop=False)
    # image = np.asarray( image )
    # print (image)
    Width = image.get().shape[1]
    Height = image.get().shape[0]
    net.setInput(blob)

    
    outs = net.forward(getOutputsNames(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    car, bike, bus, truck = 0, 0, 0, 0

    for out in outs:

        for detection in out:
    
            #classes scores starts from index 5
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
    
                if class_id==2:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
                    car=car+1                    
                        
                elif class_id==3:
                    bike=bike+1
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
                    bike=bike+1
    
                elif class_id==5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
                    bus=bus+1
    
                elif class_id==7:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
                    truck=truck+1

    # apply  non-maximum suppression algorithm on the bounding boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        j = i[0]
       
        box = (boxes[j])
       
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_pred(image, class_ids[j], confidences[j], round(x), round(y), round(x+w), round(y+h))


    # image = np.asarray(image)
    # cv2.imshow("edges", image)
    # # cv2.waitKey()
    # print(image)
    
    # cv2.imshow('',cv2.cvtColor(cv2.UMat(image), cv2.COLOR_RGB2GRAY))
    cv2.imwrite('./detection_pred/detection{0}.png'.format(video_index),image)
    return car,bike,bus,truck
