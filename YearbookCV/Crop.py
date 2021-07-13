import cv2
import os
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import mediapipe as mp
import re


def incircle(point, radius,makeCircle):
    if not makeCircle:
        return True
    if (point[0] - radius) ** 2 + (point[1] - radius) ** 2 <= radius ** 2:
        return True
    else:
        return False


def CropFace(img_file_src, size, output_path=None, makeCircle = True):
    """

        :param img_file_src: image file
        :param size: diameter of final image
        :param output_path: output folder location(if nothing specified, return image as array)
        :param makeCircle: Crop as circle or square, By default True


        """

    img_initial = cv2.imread(img_file_src)
    final_img = []
    grayImg = cv2.cvtColor(img_initial, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    faces = face_cascade.detectMultiScale(grayImg, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        faces = []
        rows, cols, c = img_initial.shape
        ColCenter = int(cols / 2)
        RowCenter = int(rows / 2)
        radius = min(ColCenter, RowCenter)
        faces.append( [ColCenter, RowCenter, radius,radius])

    # print(faces)

    for face in faces:

        face_img_raw = img_initial[face[1]:face[1] + face[2], face[0]:face[0] + face[2]]

        face_img = cv2.cvtColor(face_img_raw, cv2.COLOR_BGR2BGRA)

        radius = int(face[2] / 2)

        for rows in range(face_img.shape[0]):
            for cols in range(face_img.shape[1]):
                if not incircle([rows, cols], radius,makeCircle):
                    face_img[rows][cols][3] = 0

        face_img_final = cv2.resize(face_img, (size, size))

        final_img.append(face_img_final)
    # else:
    #     blankimg = np.zeros((size, size), dtype=np.uint8)
    #     final_img.append(cv2.cvtColor(blankimg, cv2.COLOR_GRAY2BGR))

    if output_path == None:
        return final_img
    else:
        file = re.split(r"[./\\]", img_file_src)[-2:-1]

        i = 0
        for img in final_img:
            try:
                cv2.imwrite(output_path + "\\" + file[0] + str(i)+ "." + file[1], img)
            except:
                cv2.imwrite(output_path + "\\" + file[0] + str(i) + ".png", img)
            i+=1


def CropBody(img_file_src, size, output_path=None ,makeCircle = True,removeBackground = True):
    """

        :param img_file_src: image file
        :param size: diameter of final image
        :param output_path: output folder location(if nothing specified, return image as array)
        :param makeCircle: Crop as circle or square, By default True
        :param removeBackground: Removing the background via mediapipe, By default True


        """
    img = cv2.imread(img_file_src)
    rows, cols, c = img.shape
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)
        image.flags.writeable = True
        # print(results.pose_landmarks)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Find location of nose, to center circle around it
            Nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
            if Nose:
                RowCenter = int(Nose.y * rows)
                ColCenter = int(Nose.x * cols)
            else:
                RowCenter = int(rows / 2)
                ColCenter = int(cols / 2)

            # Calculates maximum possible radius size
            if cols < rows:
                radius = int(cols / 2)
                ColCenter = radius
                if RowCenter < radius:
                    RowCenter = radius
                elif rows - RowCenter < radius:
                    RowCenter = rows - radius
            else:
                radius = int(rows / 2)
                RowCenter = radius
                if ColCenter < radius:
                    ColCenter = radius
                elif cols - ColCenter < radius:
                    ColCenter = cols - radius

            segment = SelfiSegmentation(0)
            if removeBackground:
                ImageOut = segment.removeBG(img, (255, 255, 255))
            else:
                ImageOut = img


            # Crops image
            face_img_raw = ImageOut[RowCenter - radius:RowCenter + radius, ColCenter - radius:ColCenter + radius]

            # Convert to include an alpha value
            face_img = cv2.cvtColor(face_img_raw, cv2.COLOR_BGR2BGRA)

            for rows in range(face_img.shape[0]):
                for cols in range(face_img.shape[1]):
                    if not incircle([rows, cols], radius, makeCircle):
                        face_img[rows][cols][3] = 0

            face_img_final = cv2.resize(face_img, (size, size))
        else:

            ColCenter = int(cols / 2)
            RowCenter = int(rows / 2)
            radius = min(ColCenter,RowCenter)
            if removeBackground:
                segment = SelfiSegmentation(0)
                img = segment.removeBG(img, (255, 255, 255))


            face_img_raw = img[RowCenter - radius:RowCenter + radius, ColCenter - radius:ColCenter + radius]

            face_img_raw = cv2.cvtColor(face_img_raw, cv2.COLOR_BGR2BGRA)
            for rows in range(face_img_raw.shape[0]):
                for cols in range(face_img_raw.shape[1]):
                    if not incircle([rows, cols], radius, makeCircle):
                        face_img_raw[rows][cols][3] = 0

            face_img_final = cv2.resize(face_img_raw, (size, size))
        if output_path == None:
            return face_img_final
        else:
            file = re.split(r"[./\\]", img_file_src)[-2:-1]


            try:
                cv2.imwrite(output_path + "\\" + file[0] + "." + file[1], face_img_final)
            except:
                cv2.imwrite(output_path + "\\" + file[0] + ".png", face_img_final)


def CropAll(inputPath, outputPath, type=0, makeCircle = True,removeBackground = True):
    """

        :param inputPath: image folder path

        :param outputPath: output folder path
        :param type: type of crop, 0 to crop body, 1 to get face crop , default is 0
        :param makeCircle: Crop as circle or square, By default True


        """
    for file in os.listdir(inputPath):
        img_initial = cv2.imread(inputPath + "\\" + file)
        rows, cols, c = img_initial.shape
        size = int(min(rows, cols))

        if type == 0:
            CropBody(inputPath + "\\" + file, size, outputPath,makeCircle,removeBackground)
        else:
            CropFace(inputPath + "\\" + file, size, outputPath,makeCircle)


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(BASE_DIR)

    inputPath = os.path.join(BASE_DIR + "\\Input")
    outputPath = os.path.join(BASE_DIR + "\\Output")

    CropAll(inputPath,outputPath,1,True,False)


    # for file in os.listdir(inputPath):
    # file = os.listdir(inputPath)[0]
    # print(file)
    # # img_initial = cv2.imread(inputPath + "\\" + file)
    # outImg = CropBody(inputPath + "\\" + file, 300)
    # # outImg = outImg[0]
    # if not cv2.imwrite(os.path.join(outputPath + "\\" + file), outImg):
    #     raise Exception("Could not write image")
