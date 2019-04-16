# Essential Python Funtions to Run UI
# Developer : Shashank Sharma

import cv2

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
        

