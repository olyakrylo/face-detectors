import cv2
from matplotlib import pyplot as plt
from cv2.data import haarcascades
from imutils import face_utils
import dlib


class FaceDetector:

    def __init__(self, img_path):
        self.img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        self.small = self.img.shape[1] < 100

    def template_matching(self, template_path, method_str):
        img = self.img.copy()
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        w, h = template.shape[:-1]
        method = eval("cv2.{}".format(method_str))
        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + h, top_left[1] + w)

        line_width = 2 if self.small else 5
        cv2.rectangle(img, top_left, bottom_right, 255, line_width)

        plt.imsave("result_tm.jpg", img[:, :, ::-1], format="jpg")

    def viola_jones(self):
        face_cascade = cv2.CascadeClassifier("{}haarcascade_frontalface_default.xml".format(haarcascades))
        eye_cascade = cv2.CascadeClassifier("{}haarcascade_eye.xml".format(haarcascades))

        scale = 1.01 if self.small else 1.3
        neighbors = 1 if self.small else 5
        min_size = 2 if self.small else 30
        img = self.img.copy()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scale, neighbors, minSize=(min_size, min_size))

        line_width = 1 if self.small else 5
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), line_width)
            eyes = eye_cascade.detectMultiScale(gray, 1.3, line_width)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), line_width)

        plt.imsave("result_vj.jpg", img[:, :, ::-1], format="jpg")

    def sym_lines(self):
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        image = self.img.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        rects = detector(gray, 1)

        line_width = 1 if self.small else 5
        for (i, rect) in enumerate(rects):
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), line_width)

            (x1, y1) = shape[27]
            (x2, y2) = shape[8]
            (x3, y3) = shape[37]
            (x5, y5) = shape[44]
            x4 = x2 - x1 + x3
            y4 = y2 - y1 + y3
            x6 = x2 - x1 + x5
            y6 = y2 - y1 + y5

            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), line_width)
            cv2.line(image, (x3, y3), (x4, y4), (255, 0, 0), line_width)
            cv2.line(image, (x5, y5), (x6, y6), (255, 0, 0), line_width)

        plt.imsave("result_sym.jpg", image[:, :, ::-1], format="jpg")
