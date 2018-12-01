import cv2
import datetime
from time import sleep
from imutils.video import VideoStream

def write_to_video(name, images):
    height, width, layers = images[0][1].shape
    video_fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(name, video_fourcc, 30, (width,height))
    for time_stamp, image in images:
        video.write(image)
    video.release()
    cv2.destroyAllWindows()

def write_to_picseries(series_name, images):
    height, width, layers = images[0][1].shape
    for time_stamp, image in images:
        cv2.imwrite(f'{series_name}{time_stamp}.png',image)
    cv2.destroyAllWindows()

def record_webcam(duration, frame_rate):
    vs = VideoStream()
    vs.start()
    n = 0
    images = []
    while n < duration * frame_rate:
        image = vs.read()
        if vs.read() is not None:
            images.append((datetime.datetime.now(), image))
            n += 1
        sleep(1/frame_rate)
    vs.stop()
    return images
