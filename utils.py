# utils.py

from pathlib import Path
from typing import Union, Callable

def makedir(dirpath: Union[str, Path], parents=True, exist_ok=True, verbose=True) -> Path:
    if not isinstance(dirpath, Path):
        dirpath = Path(dirpath)
    if dirpath.exists():
        return dirpath
    else:
        dirpath.mkdir(parents=parents, exist_ok=exist_ok)
        if verbose:
            print('Created: ', dirpath)
        return dirpath

def snake2camel(s):
    "Convert snake_case to CamelCase"
    return ''.join(s.title().split('_'))