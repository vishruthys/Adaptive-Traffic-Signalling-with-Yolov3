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
import numpy as np

def crop(img, pts):
    mask = np.ones(img.shape, dtype = "uint8")
    points=np.asarray(pts)
    points=points.astype(int)
    cv2.fillPoly(mask, [points], (255,255,255))
    cropImg = cv2.bitwise_and(img, mask)
    return cv2.UMat(cropImg)

'''
Unused Functions in this Project

def VideoSampler(video,time):
    cap = cv2.VideoCapture(video)
    fps=cap.get(cv2.CAP_PROP_FPS)	
    cap.set(1, (time*fps))
    ret, frame = cap.read()
    return frame


def cord(newimg):
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.imshow(cv2.cvtColor(newimg, cv2.COLOR_BGR2RGB))
    print("Please click")
    x = plt.ginput(4)
    print("clicked", x)
    plt.close()
    return x

def Selector(a):
    mask = np.ones(a.shape, dtype = "uint8")
    points=np.asarray(cord(a))
    points=points.astype(int)
    cv2.fillPoly(mask, [points], (255,255,255))
    maskedImg = cv2.bitwise_and(a, mask)
    return maskedImg
'''


