from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2
from matplotlib import pyplot as plt


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

image = cv2.imread("./img/hair.jpg")
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

rects = detector(gray, 1)

for (i, rect) in enumerate(rects):
	shape = predictor(gray, rect)
	shape = face_utils.shape_to_np(shape)
	(x, y, w, h) = face_utils.rect_to_bb(rect)
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

	for (x, y) in shape:
		cv2.circle(image, (x, y), 1, (0, 0, 255), 2)

plt.imsave("result.jpg", image[:, :, ::-1], format="jpg")