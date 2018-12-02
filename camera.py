import numpy as np
import cv2


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

        self.face_cascade = cv2.CascadeClassifier('/home/kevin/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
        self.profile_cascade = cv2.CascadeClassifier('/home/kevin/opencv/data/haarcascades/haarcascade_profileface.xml')
        self.eye_cascade = cv2.CascadeClassifier('/home/kevin/opencv/data/haarcascades/haarcascade_eye.xml')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        self.bounding_boxes(image, gray)   

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def bounding_boxes(self, img, gray_image):
        faces = self.face_cascade.detectMultiScale(gray_image, 1.3, 5)
        profiles = self.profile_cascade.detectMultiScale(gray_image, 1.3, 5)

        '''
        if isinstance(faces, np.ndarray):
            #print(faces)
            print('faces.shape')
            

        if isinstance(profiles, np.ndarray):
            print(profiles)
            print(profiles.shape)'''


        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray_image[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
