# define class and related functions
from copy import copy, deepcopy
from dataclasses import dataclass, field
from msilib.schema import Component
from typing import ClassVar
import numpy as np
from modules.utility import *
from modules import interface
import PyQt5.QtCore
from PyQt5.QtWidgets import QMessageBox




#TODO: add a function to update the image in the viewer
#TODO: add exception handling e.g. empty image
#TODO: add exception handling e.g. wrong image type + logging

#TODO: plan how to handle different images in the architecture
#TODO: supported types of images (bmp, jpg, dicom)

# frozen = True means that the class cannot be modified
# kw_only = True means that the class cannot be instantiated with positional arguments
@dataclass(frozen = True)
class Image:

    data: np.ndarray  # required on init
    path: str = ''
    metadata: dict = field(default_factory=dict)

    # def __post_init__(self):
    #     self.update_parameters()

    # def update_parameters(self):
    #     # TODO: calculate basic parameters (width, height, etc)
    #     pass
    def get_pixels(self):
        return self.data
    def get_formatted_metadata(self):
        # return '\n'.join([f'{key}: {value}' for key, value in self.metadata.items()])
        return "test"
    def get_img_format(self):
        return self.path.split('.')[-1]

