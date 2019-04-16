#from sel import VideoSampler
#from sel import Selector
import cv2
#import matplotlib.pyplot as plt
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


    
    

    
