import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))
img = ins_get_image('image70_1')
faces = app.get(img)
rimg = app.draw_on(img, faces)
cv2.imwrite("./result_output.jpg", rimg)