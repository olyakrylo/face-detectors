import cv2
from matplotlib import pyplot as plt


class TemplateMatcher:

    def __init__(self, template_path):
        self.template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        self.w, self.h = self.template.shape[:-1]

    def exec(self, img_path, method_str):
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        method = eval("cv2.{}".format(method_str))
        res = cv2.matchTemplate(img, self.template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + self.h, top_left[1] + self.w)

        cv2.rectangle(img, top_left, bottom_right, 255, 5)

        plt.imsave("result.jpg", img[:, :, ::-1], format="jpg")
