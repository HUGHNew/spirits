import os

from PIL import Image

def division(image: Image.Image, row:int, column:int, output_dir:str):
    w, h = image.size
    w_delta, h_delta = w//column, h//row
    if os.path.exists(output_dir):
        if not os.path.isdir(output_dir):
            raise RuntimeError(f"{output_dir} exists and isn't a folder")
    else:
        os.mkdir(output_dir)
    for r in range(row):
        for c in range(column):
            left, upper = c * w_delta, r * h_delta
            image.crop((left, upper, left+w_delta, upper+h_delta)).save(os.path.join(output_dir,f"{r}-{c}.jpg"))

