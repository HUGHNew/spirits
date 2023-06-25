from typing import List, Optional
from typing_extensions import Annotated

import typer

from utils import partition, get_image
from gather import compose
from scatter import division

spirits = typer.Typer()
OptionalInt=Annotated[Optional[int], typer.Argument()]

@spirits.command()
def gather(output: str,
           column:Optional[int]=0, row:Optional[int]=0,
           images: Annotated[Optional[List[str]], typer.Argument()] = None,
           file: Optional[str]=None,):
    if not images:
        if not file:
            raise RuntimeError("specify images or images file")
        else:
            with open(file) as f:
                images = [
                    line.strip()
                    for line in f.readlines()
                ]
            pass
    elif file:
        raise RuntimeError("specify images or images file")
    image_matrix = partition(images, row, column)
    compose(image_matrix, output)

@spirits.command()
def scatter(image_ref:str, row:int, column:int, output_dir:str="output"):
    image = get_image(image_ref)
    if row <= 0 or column <= 0:
        raise RuntimeError(f"row and column must be greater than 0")
    division(image, row, column, output_dir)

if __name__ == "__main__":
    spirits()