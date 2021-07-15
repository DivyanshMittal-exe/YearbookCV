import os
import cv2 as cv
import mediapipe as mp
from YearbookCV.utils import makeFolder, collect_image_files


class AutoAligner():

    def __init__(self):

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.mp_holistic = mp.solutions.holistic
        self.mp_face_detection = mp.solutions.face_detection

    def align_image(self, img, min_face_detection_confidence=0.5, min_pose_detection_confidence=0.5):
        """
        :param img: image to align
        :param min_face_detection_confidence: confidence for face detection in the image
        :param min_pose_detection_confidence: confidence for pose detection in the image
        :return: aligned image
        """
        with self.mp_pose.Pose(static_image_mode=True, model_complexity=2,
                               min_detection_confidence=min_pose_detection_confidence) as pose:
            image = img
            image_height, image_width, _ = image.shape

            results = pose.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

            if not results.pose_landmarks:
                i = 0
                while (True):
                    mp_face_detection = self.mp_face_detection

                    with mp_face_detection.FaceDetection(model_selection=1,
                                                         min_detection_confidence=min_face_detection_confidence) as face_detection:

                        if i == 4:
                            return image
                        results2 = face_detection.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))
                        if not results2.detections:
                            i += 1
                            image = cv.rotate(image, rotateCode=0)
                            continue

                        return image

            n = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.NOSE].y
            r = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_SHOULDER].y
            l = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_SHOULDER].y

            if n < r and n < l:
                pass
            elif n > r and n > l:
                image = cv.rotate(image, rotateCode=1)
            elif n < r and n > l:
                image = cv.rotate(image, rotateCode=0)
            else:
                image = cv.rotate(image, rotateCode=2)

            return image


def auto_align(input_file, output_file, min_face_detection_confidence=0.5, min_pose_detection_confidence=0.5):
    """
    :param input_file: file containing images
    :param output_file: file to store aligned images
    :param min_face_detection_confidence: confidence for face detection in the image
    :param min_pose_detection_confidence: confidence for pose detection in the image

    """
    images = collect_image_files(input_file)
    # makeFolder(output_file)

    path = output_file

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    mp_holistic = mp.solutions.holistic

    with mp_pose.Pose(static_image_mode=True, model_complexity=2,
                      min_detection_confidence=min_pose_detection_confidence) as pose:

        for idx, file in enumerate(images):

            image = cv.imread(input_file + "\\" + file)
            filename, file_ext = os.path.splitext(images[idx])
            image_height, image_width, _ = image.shape

            results = pose.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

            if not results.pose_landmarks:
                i = 0
                while (True):

                    mp_face_detection = mp.solutions.face_detection
                    with mp_face_detection.FaceDetection(model_selection=1,
                                                         min_detection_confidence=min_face_detection_confidence) as face_detection:

                        if i == 4:
                            try:
                                cv.imwrite(path + '\\' + filename + file_ext, image)
                            except:
                                cv.imwrite(path + '\\' + filename + ".png", image)
                            break

                        results2 = face_detection.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

                        if not results2.detections:
                            i += 1
                            image = cv.rotate(image, rotateCode=0)
                            continue

                        try:
                            cv.imwrite(path + '\\' + filename + file_ext, image)
                        except:
                            cv.imwrite(path + '\\' + filename + ".png", image)
                        break

                continue

            n = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE].y
            r = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER].y
            l = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER].y

            if n < r and n < l:
                pass
            elif n > r and n > l:
                image = cv.rotate(image, rotateCode=1)
            elif n < r and n > l:
                image = cv.rotate(image, rotateCode=0)
            else:
                image = cv.rotate(image, rotateCode=2)

            try:
                cv.imwrite(path + '\\' + filename + file_ext, image)
            except:
                cv.imwrite(path + '\\' + filename + ".png", image)