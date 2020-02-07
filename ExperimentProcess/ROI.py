import cv2
import numpy as np
import os, glob


def ROI(from_path, to_path, up, left, h, w, format = "bmp"):
    names = os.path.join(from_path, '*.'+format)
    #print(names)
    images = sorted(glob.glob(names))
    #print(images)
   
    for img in images:
        roi = cv2.imread(img)[up:up+h,left:left+w] 
        im = os.path.split(img)[-1]
        print(im)
        cv2.imwrite(os.path.join(to_path, im), roi)
        print('done!')

ROI('C:\\Users\\windows\\Desktop\\3\\Cam1', 'G:\\Project6\\ZhongLv\\\BM\\1mm_min\\3\\Cam1', 200, 0, 600,1628)