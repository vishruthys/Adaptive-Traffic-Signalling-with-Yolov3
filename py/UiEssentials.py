#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
#       Essentials Methods for FrontEnd and Backend
#       Developer : Shashank Sharma
# =============================================================================
#       Copyright (C) 2019  Shashank Sharma, 
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
import subprocess
import os

def qimg2cv(q_img):
    # =====================================================================
    # Converts QImage to OpenCV Format
    # =====================================================================
    q_img.save('temp.png', 'png')
    mat = cv2.imread('temp.png')
    return mat

supported_video_formats = ('.avi', '.mp4', '.mov', '.3gp', '.flv', '.mvp','.mpg4',
                          '.mpeg', '.mpeg4','.mkv','.m4u','.f4v')

def isVideoFile(file_path):
    # =========================================================================
    # Returns if the selected file is a video file or not
    # =========================================================================
    return '.' + file_path.split('.')[-1] in supported_video_formats
        
def getScreenResolution():
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    return output

def setScreenResolution(width, height):
    os.system('xrandr -s {}x{}'.format(width, height))