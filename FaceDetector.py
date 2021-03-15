import cv2
from matplotlib import pyplot as plt
from cv2.data import haarcascades
import numpy as np


def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return x, y, w, h


def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords


class FaceDetector:

    def __init__(self, img_path):
        self.img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    def template_matching(self, template_path, method_str):
        img = self.img.copy()
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        w, h = template.shape[:-1]
        method = eval("cv2.{}".format(method_str))
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + h, top_left[1] + w)

        cv2.rectangle(img, top_left, bottom_right, 255, 5)

        plt.imsave("result_tm.jpg", img[:, :, ::-1], format="jpg")

    def viola_jones(self):
        face_cascade = cv2.CascadeClassifier("{}haarcascade_frontalface_default.xml".format(haarcascades))
        eye_cascade = cv2.CascadeClassifier("{}haarcascade_eye.xml".format(haarcascades))

        img = self.img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)
            eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 5)

        plt.imsave("result_vj.jpg", img[:, :, ::-1], format="jpg")
