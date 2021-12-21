import numpy as np
import cv2
from PIL import Image, ImageFilter

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

def flat_filter(img)
    img = pil2cv(img)
    bgr = cv2.split(img)
    res = []
    for c in bgr:
        dst = cv2.blur(c, (50, 50)) 

        avg_hist = c.mean()
        ffc = (c/dst)*avg_hist
        res.append(ffc)

    flaten = cv2.merge(res)
    return cv2pil(flaten)

def noise_filter(img)
    img = img.filter(ImageFilter.MaxFilter)
    img = img.filter(ImageFilter.MinFilter)
