import cv2
import os
import numpy as np



def edge_mask(img, line_size, blur_value):
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      gray_blur = cv2.medianBlur(gray, blur_value)
      edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
      return edges

def Countours(image):
    contoured_image = image
    gray = cv2.cvtColor(contoured_image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 200, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2:]
    cv2.drawContours(contoured_image, contours, contourIdx=-1, color=6, thickness=1)
    return contoured_image

def ColourQuantization(image, K=9):
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    compactness, label, center = cv2.kmeans(Z, K, None, criteria, 1, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((image.shape))
    return res2

def BlurredCartoonFilter(inputPath, outputPath):
    """

        :param inputPath: image folder path

        :param outputPath: output folder path


        """
    for file in os.listdir(inputPath):
        img = cv2.imread(inputPath + "\\" + file)
        line_size = 7
        blur_value = 7
        edges = edge_mask(img, line_size, blur_value)
        total_color = 8
        k = total_color
        data = np.float32(img).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        blurred = cv2.bilateralFilter(result, d=10, sigmaColor=250, sigmaSpace=250)
        cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

        try:
            cv2.imwrite(outputPath + "\\" + file , cartoon)
        except:
            cv2.imwrite(outputPath + "\\" + file+ ".png", cartoon)

def CartoonFilter(inputPath, outputPath):
    """

        :param inputPath: image folder path

        :param outputPath: output folder path


        """
    for file in os.listdir(inputPath):
        image = cv2.imread(inputPath + "\\" + file)
        coloured = ColourQuantization(image)
        contoured = Countours(coloured)
        final_image = contoured

        try:
            cv2.imwrite(outputPath + "\\" + file, final_image)
        except:
            cv2.imwrite(outputPath + "\\" + file + ".png", final_image)
        # if not cv2.imwrite(outputPath + "\\" + file , final_image):
        #     cv2.imwrite(outputPath + "\\" + file+ ".png", final_image)

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(BASE_DIR)

    inputPath = os.path.join(BASE_DIR + "\\Input")
    outputPath = os.path.join(BASE_DIR + "\\Output")
    BlurredCartoonFilter(inputPath, outputPath)


