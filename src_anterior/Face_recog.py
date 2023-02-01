import os
import cv2
import numpy as np
import face_recognition
import dnn

alg = "haarcascade_frontalface_default.xml"
haar_cascade = cv2.CascadeClassifier(alg)

f_list = os.listdir("./images")
for i in f_list:
    file_name="./images/%s"%(i)
    im = cv2.imread(file_name)
    _, bboxes = dnn.FaceDetector().process_frame(im, threshold=0.4) 

    # face_locations is now an array listing the co-ordinates of each face!
    print("I found {} face(s) in this photograph.".format(len(bboxes)))

    for i in bboxes: 

        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()