import imageio
import os

def writeGif(path, type='bmp'):
    files = os.listdir(path)
    frames = []
    images = sorted([img for img in files if img.endswith('.'+type)])
    
    for ii, img in enumerate(images):
        if ii % 30 == 0:
            imgItem = imageio.imread(img)
            #print(imgItem)
            frames.append(imgItem)

    imageio.mimsave('gif.gif', frames, duration = 1/2.5)
    
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 1:
        print('error')
        sys.exit(1)
    
    writeGif(os.getcwd(), sys.argv[1])
    print('ok')