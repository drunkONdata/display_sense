import datetime
from time import sleep
import cv2
from imutils.video import VideoStream


def write_to_video(name, images):
    """
    This function writes a list of time_stamp,images into a video named using
    the name parameter and the first time stamp in the image list.

    Args:
        name: Name of the video as a string.
        images: A list of tuples containing time stamps and
                images, (time stamp, image).

    Returns:
        None
    """
    time_name = f'{images[0][0]}{name}'
    height, width = images[0][1].shape[:2]
    video_fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(time_name, video_fourcc, 30, (width, height))
    for time_stamp, image in images:
        video.write(image)
    video.release()
    cv2.destroyAllWindows()


def write_to_picseries(series_name, images):
    """
    This function writes a list of time_stamp,images into a collection of
    saved images having the of time stamp + series name parameter.

    Args:
        name: Name of the picture series as a string.
        images: A list of tuples containing time stamps and
                images, (time stamp, image).

    Returns:
        None
    """
    for time_stamp, image in images:
        cv2.imwrite(f'{time_stamp}{series_name}', image)
    cv2.destroyAllWindows()


def record_webcam(duration, frame_rate):
    """
    Uses the local webcam to record for the duration and frame rate specified.
    Returns a list of tuples containing a time stamp and an image.

    Args:
        duration: The amount of time to record for in seconds as an int.
        frame_rate: The number of images to record each second as an int.

    Returns:
        A list of tuples containing a time stamp an image,
        (time stamp,(image)).
    """
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
