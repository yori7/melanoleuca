from __future__ import unicode_literals, print_function, absolute_import
from PIL import Image, ImageChops
import numpy as np

#def get_img(fname):
#    img = Image.open(fname)
#    return img

def change_img(fname, r_min, g_min, b_min, r_max, b_max, g_max):
    img = Image.open(fname)
    img = img.convert('RGB')
    r, g, b = img.split()

    _r = r.point(lambda _: 1 if r_min <= _ <= r_max else 0, mode="1")
    _g = g.point(lambda _: 1 if g_min <= _ <= g_max else 0, mode="1")
    _b = b.point(lambda _: 1 if b_min <= _ <= b_max else 0, mode="1")

    mask = ImageChops.logical_and(_r, _g)
    mask = ImageChops.logical_and(_b, mask)
#    mask = dilation(mask)

    dst_color = (255, 0, 0)
    img.paste(Image.new("RGB", img.size, dst_color), mask=mask)

    return img, mask

#def dilation(img):
#  img = img.convert("L")
#  w, h = img.size
#  image_pixcels = np.array(list(img.getdata())).reshape(h, w,)
#  filtered_pixcels = np.zeros((h, w,))
#  for x in range(w):
#    for y in range(h):
#      x1 = max(0, x - 1)
#      x2 = min(x + 1, w - 1)
#      y1 = max(0, y - 1)
#      y2 = min(y + 1, h - 1)
#      if (image_pixcels[y1:y2 + 1, x1:x2 + 1] == 255).any():
#        filtered_pixcels[y][x] = 255
#      else:
#        filtered_pixcels[y][x] = 0
#  filtered_img = Image.new('L', (w, h))
#  filtered_img.putdata(filtered_pixcels.reshape(w * h, 1))
#  return filtered_img