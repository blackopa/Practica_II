import cv2
import sys
import os
#f_list = os.listdir("./images")
#for i in f_list:
    #imagePath="./images%s"%(i)
imagePath = sys.argv[1]
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=3,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
) 

print("Found {0} Faces!".format(len(faces)))
...
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
status = cv2.imwrite('faces_detected.jpg', image)
print ("Image faces_detected.jpg written to filesystem: ",status)
