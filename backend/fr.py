from sel import VideoSampler
from sel import Selector
import cv2
import matplotlib.pyplot as plt
import numpy as np


def getOutputsNames(net):
    layersNames = net.getLayerNames()
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# draw rectangle
def draw_pred(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 5)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Define a window to show the cam stream on it
# window_title= "Traffic Detector"
# cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)


# Load names classes
options = {"config": "./yolov3.cfg",
           "weights": "./yolov3.weights",
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
    
def detection():
    
    
    usimage = VideoSampler('./video/t1.mp4',4)
    
    image=Selector(usimage)
    
    redundimage = cv2.bitwise_xor(usimage, image)
    
    
    
    blob = cv2.dnn.blobFromImage(image, 1.0/255.0, (416,416), [0,0,0], True, crop=False)
    Width = image.shape[1]
    Height = image.shape[0]
    net.setInput(blob)
    
    outs = net.forward(getOutputsNames(net))
    
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4
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
            if confidence > 0.5:
    
                if class_id==3:
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
            if confidence > 0.5:
    
                 if class_id==5:
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
            if confidence > 0.5:
    
                if class_id==7:
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
    
    # nms
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    
    for i in indices:
        j = i[0]
    
        box = (boxes[j])
    
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_pred(image, class_ids[j], confidences[j], round(x), round(y), round(x+w), round(y+h))
    
    
    print("car=",car)
    print("bike=",bike)
    print("bus=",bus)
    print("truck=",truck)
    print("total=",car+bus+bike+truck)
    
    bike=0.5*bike
    bus=4*bus
    truck=5*truck
    print("normalized total=",car+bus+bike+truck)
    
    #    t, _ = net.getPerfProfile()
    
    #label = 'Inference time: %.2f ms' % (t * 1000.0 / cv2.getTickFrequency())
    #cv2.putText(image, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
    #cv2.imwrite("f2.jpg", image)
    #cv2.imshow(window_title,image)
    #cv2.waitKey(1000)
    
#    final=cv2.bitwise_or(image,redundimage)
#    
#    fig, ax = plt.subplots(figsize=(20, 10))
#    ax.imshow(cv2.cvtColor(final, cv2.COLOR_BGR2RGB))
#    plt.show()
    return car,bike,bus,truck
    
    

    
