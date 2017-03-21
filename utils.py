# coding:utf-8
from PIL import Image
import colorsys
import os


def get_color(im):
    '''
    Get the main color of a picture, by this color we can judge the status of a video is finished or not.
    '''
    im = Image.open(im)
    im = im.convert('RGBA')

    # generate thumbnails, reduce cpu pressure
    im.thumbnail((200, 200))
    max_score = None
    dominant_color = None
    for count, (r, g, b, a) in im.getcolors(im.size[0] * im.size[1]):
        saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
        y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
        y = (y - 16.0) / (235 - 16)
        score = (saturation + 0.1) * count
        if score > max_score:
            max_score = score
            dominant_color = (r, g, b)

    return dominant_color


def cut_vcode(picture, out_path, a, b, c, d):
    '''
    Cut the picture to get a smaller one, maybe just 5x5.
    '''
    im = Image.open(picture)
    im.getbbox()
    region = (a, b, c, d)
    cropImg = im.crop(region)
    cropImg.save(out_path)
