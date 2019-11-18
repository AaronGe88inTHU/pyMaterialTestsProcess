import os 
import glob
import shutil

def filter_image(path, interval, format = "tif"):
    os.chdir(path)
    imgs_names = sorted(glob.glob("*."+format))
    
    count = len(imgs_names)
    sub_set = slice(0, count, interval)
    image_sub = imgs_names[sub_set]
    print(image_sub)
    sub_path = os.path.join(path, 'subSet')
    os.mkdir(sub_path)
    for ii in image_sub:
        shutil.copyfile(ii, os.path.join(sub_path, ii))

filter_image('/Volumes/WTG/1e-04', 5)