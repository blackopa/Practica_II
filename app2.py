import cv2
import numpy as np
import insightface
from pathlib import Path
import os
import io
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))
f_list = os.listdir("./face_scrapper/insightface/data/images/imagesinformeFinal5396.pdf")
for i in range(len(f_list)):
    file_name=(os.path.basename(f_list[i]).split('.')[0])
    img = ins_get_image(file_name)
    faces = app.get(img)
    rimg = app.draw_on(img, faces)
    cv2.imwrite(f"./resultados/result_output{file_name}.jpg", rimg)