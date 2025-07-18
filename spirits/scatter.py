import os
from typing import List, Tuple

from PIL import Image

from .utils import get_image

PIXEL = Tuple[int, int, int]


def division_by_slice(
    image: Image.Image, row_slice: List[int], column_slice: List[int]
) -> List[List[Image.Image]]:
    results = []
    for row_idx in range(len(row_slice) - 1):
        row_img = []
        for col_idx in range(len(column_slice) - 1):
            img = image.crop(
                (
                    column_slice[col_idx],  # left
                    row_slice[row_idx],  # top
                    column_slice[col_idx + 1],  # right
                    row_slice[row_idx + 1],  # bottom
                )
            )
            row_img.append(img)
        results.append(row_img)
    return results


def poor_edge_detect(data: List[PIXEL]) -> int:
    # threshold = 140  # 256*3* 20%
    threshold = 20
    # print(data, end='\t')
    for idx in range(len(data) - 1):
        if abs(sum(data[idx]) - sum(data[idx + 1])) > threshold:
            return idx
    return -1


def division(image_ref: str, row: int, column: int, output_dir: str, flex_range: int):
    image = get_image(image_ref)
    ext_name = image_ref.split(".")[-1]
    w, h = image.size
    w_delta, h_delta = w // column, h // row
    if os.path.exists(output_dir):
        if not os.path.isdir(output_dir):
            raise RuntimeError(f"{output_dir} exists and isn't a folder")
    else:
        os.mkdir(output_dir)

    row_slice = [max(i * h_delta - 1, 0) for i in range(row + 1)]
    column_slice = [max(i * w_delta - 1, 0) for i in range(column + 1)]
    if flex_range != 0:
        img_data = image.getdata() # 1-D sequence with shape [w, h]
        # I assume that it's a standard grid image.
        for idx, col_idx in enumerate(column_slice[1:-1]):
            data = [img_data[i] for i in range(col_idx - flex_range, col_idx + flex_range)]
            edge_idx = poor_edge_detect(data)
            if edge_idx != -1:
                column_slice[idx+1] += edge_idx - flex_range

        for idx, row_idx in enumerate(row_slice[1:-1]):
            data = [img_data[i*w] for i in range(row_idx - flex_range, row_idx + flex_range)]
            edge_idx = poor_edge_detect(data)
            if edge_idx != -1:
                row_slice[idx+1] += edge_idx - flex_range

    results = division_by_slice(image, row_slice, column_slice)
    for i, row_img in enumerate(results):
        for j, img in enumerate(row_img):
            img.save(os.path.join(output_dir, f"{i}-{j}.{ext_name}"))
