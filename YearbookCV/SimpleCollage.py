import numpy as np
import random
import os
import cv2
import operator
from YearbookCV.Crop import CropBody


def SimpleCollage(inputPath,outputPath,size,makeCircle = True,array = None,removeBackground = False,filename = "Collage.png"):
    """

        :param inputPath: image folder path
        :param outputPath: output folder path
        :param size: Specify the final image size as (rows,columns) tuple
        :param array: Pass a numpy array with 1s at the position you want the image and 0s at the place to leave blank
        :param makeCircle: Crop as circle or square
        :param removeBackground: Specify removing background or not, by default false
        :param filename: Filename of the final collage, by default "Collage.png"

        """
    images_files = os.listdir(inputPath)
    if array == None:
        array = np.ones((8,8))

    arrayShape = array.shape

    rowsize = size[0]/arrayShape[0]
    colsize = size[1]/arrayShape[1]

    radius = int(min(rowsize,colsize)/2)

    final_img = np.zeros((size[0],size[1],4),dtype=np.uint8)



    i = 0
    max = len(images_files)
    for row in range(arrayShape[0]):
        for col in range (arrayShape[1]):
            if i >= max:
                break
            if array[row,col] == 1:

                img_out = CropBody(inputPath + "\\" + images_files[i], 2*radius,makeCircle=makeCircle,removeBackground=removeBackground)
                x_locn = int((row+0.5)*rowsize)
                y_locn = int((col + 0.5) * colsize)
                final_img[x_locn-radius:x_locn+radius,y_locn-radius:y_locn+radius,] = img_out
                i+=1



    try:
        cv2.imwrite(os.path.join(outputPath + "\\ "+ filename ), final_img)
    except:
        cv2.imwrite(os.path.join(outputPath + "\\ " + filename +".png"), final_img)

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(BASE_DIR)

    inputPath = os.path.join(BASE_DIR + "\\Input")
    outputPath = os.path.join(BASE_DIR + "\\Output")


    SimpleCollage(inputPath,outputPath,(2000,3000),True)


