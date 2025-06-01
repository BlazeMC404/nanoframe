"""
Nanoframe: A lightweight, dependency-free data processing library.
"""

__version__ = "0.1.0"
__author__ = "BlazeMC404"
__license__ = "MIT"

from .frame import NanoFrame
from .series import NanoSeries
from .io import read_csv, read_json, to_csv, to_json
from . import utils

__all__ = [
    "NanoFrame",
    "NanoSeries",
    "read_csv",
    "read_json",
    "to_csv",
    "to_json",
    "utils"
]