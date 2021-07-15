import os
import cv2 as cv
import mediapipe as mp
import numpy as np
from YearbookCV.utils import makeFolder, collect_image_files


class SelfiSegmentation():

    def __init__(self, model=1):
        """
        :param model: model type 0 or 1. 0 is general 1 is landscape(faster)
        """
        self.model = model
        self.mpDraw = mp.solutions.drawing_utils
        self.mpSelfieSegmentation = mp.solutions.selfie_segmentation
        self.selfieSegmentation = self.mpSelfieSegmentation.SelfieSegmentation(self.model)

    def removeBG(self, img, imgBg=(255, 255, 255), threshold=0.1):
        """
        :param img: image to remove background from
        :param imgBg: BackGround Image
        :param threshold: higher = more cut, lower = less cut
        :return: background removed image
        """
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = self.selfieSegmentation.process(imgRGB)
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) > threshold
        if isinstance(imgBg, tuple):
            _imgBg = np.zeros(img.shape, dtype=np.uint8)
            _imgBg[:] = imgBg
            imgOut = np.where(condition, img, _imgBg)
        else:
            imgOut = np.where(condition, img, imgBg)
        return imgOut


def remove_background(input_file, output_file, background_img=(255, 255, 255), model=0, threshold=0.1):
    """
    :param input_file: file containing images
    :param output_file: file to store background removed images
    :param background_img: image to set for the background
    :param model: model type 0 or 1. 0 is general 1 is landscape(faster)
    :param threshold: higher = more cut, lower = less cut
    """

    images = collect_image_files(input_file)
    # makeFolder(output_file)

    segmentor = SelfiSegmentation(model)

    path = output_file
    for idx, file in enumerate(images):

        img = cv.imread(input_file + "\\" + file)
        filename, file_ext = os.path.splitext(images[idx])
        imgOut = segmentor.removeBG(img, background_img, threshold)

        try:
            cv.imwrite(path + '\\' + filename + file_ext, imgOut)
        except:
            cv.imwrite(path + '\\' + filename + ".png", imgOut)