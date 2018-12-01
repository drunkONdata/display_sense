def write_to_picseries(images, series_name):
    height, width, layers = images[0].shape

    for frame, image in enumerate(images):
        cv2.imwrite(f'{series_name}{frame}.png',image)
