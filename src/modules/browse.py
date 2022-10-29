import imp


from PyQt5.QtWidgets import QFileDialog
import matplotlib.pyplot as plt
import numpy as np
from modules import interface
from modules.image import *
from modules.importers import *



def browse_window(self, image_idx=1):
    self.filename = QFileDialog.getOpenFileName(
        None, 'open the image file', './', filter="Raw Data(*.bmp *.jpg *.dicom)")
    path = self.filename[0]
    print_debug("Selected path: " + path)

    if path == '':
        # raise Warning("No file selected")
        return

    # select an image importer based on the file extension
    importer = read_importer(path)

    # import the image into an image object
    self.image1 = importer.import_image(path)

    # update the image and textbox in the viewer
    interface.refresh_display(self)

def read_importer(path) -> ImageImporter:
    #parse file extension
    extension = path.split('.')[-1]
    #array of supported extensions
    importers = {
        'bmp': BMPImporter(),
        'jpg': JPGImporter(),
        'dicom': DICOMImporter()
    }
    if extension in importers:
        return importers[extension]
    else:
        raise Warning("Unsupported file type")
