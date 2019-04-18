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
#       This code is part of the repo https://github.com/vishruthys/VidGUI
# =============================================================================


import cv2
import numpy as np

def getOutputsNames(net):
    layersNames = net.getLayerNames()
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Load names classes
options = {"config": "./yolov3.cfg",
           "weights": "/home/vishruthys/Project/yolov3.weights",
           "classes": "./coco.names",
           }
classes = None
with open(options["classes"], 'r') as f:
    classes = [line.strip() for line in f.readlines()]
#print(classes)

#Generate color for each class randomly
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# Define network from configuration file and load the weights from the given weights file
net = cv2.dnn.readNet(options["weights"],options["config"])
    
def detection(image):

    
    blob = cv2.dnn.blobFromImage(image, 1.0/255.0, (416,416), [0,0,0], True, crop=False)

    net.setInput(blob)
    
    outs = net.forward(getOutputsNames(net))

    car=0
    bike=0
    bus=0
    truck=0
    
    for out in outs:
        #print(out.shape)
        for detection in out:
    
            scores = detection[5:]#classes scores starts from index 5
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > 0.5:
    
                if class_id==2:
                    
                    car=car+1
                    
            if confidence > 0.5:
    
                if class_id==3:
                    
                    bike=bike+1
                    
            if confidence > 0.5:
    
                 if class_id==5:
                    
                    bus=bus+1
                    
            if confidence > 0.5:
    
                if class_id==7:
                    
                    truck=truck+1

    return car,bike,bus,truck