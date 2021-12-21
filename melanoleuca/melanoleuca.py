from __future__ import unicode_literals, print_function, absolute_import
from PIL import Image, ImageChops, ImageFilter
import cv2
import numpy as np

def change_img(fname, r_min, g_min, b_min, r_max, b_max, g_max):
    img = Image.open(fname)
    img = img.convert('RGB')
    img = flat_filter(img)
    r, g, b = img.split()

    _r = r.point(lambda _: 1 if r_min <= _ <= r_max else 0, mode="1")
    _g = g.point(lambda _: 1 if g_min <= _ <= g_max else 0, mode="1")
    _b = b.point(lambda _: 1 if b_min <= _ <= b_max else 0, mode="1")

    mask = ImageChops.logical_and(_r, _g)
    mask = ImageChops.logical_and(_b, mask)
    mask = noise_filter(mask)

    dst_color = (255, 0, 0)
    img.paste(Image.new("RGB", img.size, dst_color), mask=mask)

    return img, mask

def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image

def flat_filter(img):
    img = pil2cv(img)
    bgr = cv2.split(img)
    res = []
    for c in bgr:
        dst = cv2.blur(c, (50, 50)) 

        avg_hist = c.mean()
        ffc = (c/dst)*avg_hist
        res.append(ffc)

    flaten = cv2.merge(res)
    flaten = flaten.astype("uint8")
    return cv2pil(flaten)

def noise_filter(img):
    img = img.filter(ImageFilter.MaxFilter)
    img = img.filter(ImageFilter.MinFilter)
    img = img.filter(ImageFilter.MinFilter)
    return img
