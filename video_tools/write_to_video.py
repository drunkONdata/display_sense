def write_to_video(name, images):
    height, width, layers = images[0].shape
    video_fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(name, video_fourcc, 30, (width,height))
    for image in images:
        video.write(image)
    video.release()
