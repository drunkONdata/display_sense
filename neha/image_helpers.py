import requests

def get_img_from_url(imgurl):
    response = requests.get(imgurl)
    return response.content

def get_img_from_file(filename):
    with open(filename, 'rb') as imgfile:
        return imgfile.read()

