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

ROI('I:\\dianchike\\uni\\3\\Cam1', 'H:\\GAC\\battery\\Exp\\Alum\\uni\\3\\Cam1', 450, 0, 400,1628)