from typing import List, Optional
from typing_extensions import Annotated

import typer

from .utils import partition
from .gather import compose
from .scatter import division

spirits_cmd = typer.Typer()
OptionalInt = Annotated[Optional[int], typer.Argument()]


@spirits_cmd.command()
def gather(
    output: str,
    row: int = 0,
    column: int = 0,
    images: Annotated[Optional[List[str]], typer.Argument()] = None,
    file: Optional[str] = None,
):
    if not images:
        if not file:
            raise RuntimeError("specify images or images file")
        else:
            with open(file) as f:
                images = [line.strip() for line in f.readlines()]
            pass
    elif file:
        raise RuntimeError("specify images or images file")
    image_matrix = partition(images, row, column)
    compose(image_matrix, output)


@spirits_cmd.command(
    help="scatter image into rows and columns with flexible pixel range (There must be a clear dividing line)"
)
def scatter(
    image_ref: str,
    row: int,
    column: int,
    output_dir: str = "output",
    flex_range: int = 0,
):
    if row <= 0 or column <= 0:
        raise RuntimeError("row and column must be greater than 0")
    division(image_ref, row, column, output_dir, flex_range)


if __name__ == "__main__":
    spirits_cmd()
