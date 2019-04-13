import cv2
import numpy as np
import matplotlib.pyplot as plt

def cord(newimg):
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.imshow(cv2.cvtColor(newimg, cv2.COLOR_BGR2RGB))
    print("Please click")
    x = plt.ginput(4)
    print("clicked", x)
    #plt.show()
    plt.close()
    return x

def Selector(a):
    #newimg = cv2.imread("./t18.png")
    mask = np.ones(a.shape, dtype = "uint8")
    points=np.asarray(cord(a))
    points=points.astype(int)
    cv2.fillPoly(mask, [points], (255,255,255))
    maskedImg = cv2.bitwise_and(a, mask)
    return maskedImg

def VideoSampler(video,time):
   cap = cv2.VideoCapture(video)
   fps=cap.get(cv2.CAP_PROP_FPS)	
   #total_frames = cap.get(7)
   cap.set(1, (time*fps))
   ret, frame = cap.read()
   return frame
    
'''def merge(a,b,c):
    #maskedImg = cv2.bitwise_and(a, b)
    img2=cv2.bitwise_xor(a,b)
    fig, ax = plt.subplots(figsize=(20, 10))
    final=cv2.bitwise_or(img2,c)
    #ax.imshow(final)
	#plt.show()
    return final'''

def crop(img,pts):
    #newimg = cv2.imread("./t18.png")
    mask = np.ones(img.shape, dtype = "uint8")
    points=np.asarray(pts)
    points=points.astype(int)
    cv2.fillPoly(mask, [points], (255,255,255))
    cropImg = cv2.bitwise_and(img, mask)
    return cropImg
