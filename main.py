from FaceDetector import FaceDetector
from sklearn.datasets import fetch_olivetti_faces
from PIL import Image
import numpy as np

data_images = fetch_olivetti_faces()
img_array = data_images["data"]

for i in range(30, 40):
    img = Image.fromarray((img_array[i] * 255).round().astype(np.uint8)).resize((64, 64))
    img = img.convert("L")
    img.save("./orl/{}.jpg".format(str(i - 29)))

# fd = FaceDetector("./img/original.jpg")
#
# fd.template_matching("./img/template.jpg", "TM_CCOEFF")
# fd.viola_jones()
