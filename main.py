from FaceDetector import FaceDetector
from sklearn.datasets import fetch_olivetti_faces
from PIL import Image
import numpy as np

data_images = fetch_olivetti_faces()
img_array = data_images["data"]

for i in range(24, 60):
    image = np.reshape(img_array[i], (64, 64))
    image_pil = Image.fromarray((image * 255).astype(np.uint8), 'L')
    image_pil.save("./orl/{}.jpg".format(str(i - 23)))

# fd = FaceDetector("./img/original.jpg")
#
# fd.template_matching("./img/template.jpg", "TM_CCOEFF")
# fd.viola_jones()
