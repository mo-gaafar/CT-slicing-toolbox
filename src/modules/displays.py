from PyQt5 import QtWidgets, QtCore
import numpy as np
import pyqtgraph as pg


pg.setConfigOption('imageAxisOrder', 'row-major')


class Display:
    '''
    This class initializes the all 4 pyqtgraph elements with the desired features and necessary components.
    The self.[plane]_image attribute is the element directly accessed to show/update an image.
    '''

    def __init__(self, mw):
        Display.init_axial_plot(mw)
        Display.init_sagittal_plot(mw)
        Display.init_coronal_plot(mw)
        Display.init_oblique_plot(mw)


    def init_axial_plot(self):
        self.axial_image = pg.ImageItem()
        
        self.axial_box.setAspectLocked(True)
        self.axial_box.showAxes(False)
        self.axial_box.setMouseEnabled(x=False, y=False)
        self.axial_box.addItem(self.axial_image)

        pen = pg.mkPen(color='g', width=0.5,style=QtCore.Qt.DashLine)
        self.axial_vline = pg.InfiniteLine(angle=90, movable=True, pen=pen)
        self.axial_hline = pg.InfiniteLine(angle=0, movable=True, pen=pen)
        self.axial_oline = pg.InfiniteLine(angle=135, movable=True, pen=pen)
        self.axial_box.addItem(self.axial_vline)
        self.axial_box.addItem(self.axial_hline)
        self.axial_box.addItem(self.axial_oline)

    def init_sagittal_plot(self):
        self.sagittal_image = pg.ImageItem()
        self.sagittal_box.setAspectLocked(True)
        self.sagittal_box.showAxes(False)
        self.sagittal_box.setMouseEnabled(x=False, y=False)
        self.sagittal_box.addItem(self.sagittal_image)

    def init_coronal_plot(self):
        self.coronal_image = pg.ImageItem()
        self.coronal_box.setAspectLocked(True)
        self.coronal_box.showAxes(False)
        self.coronal_box.setMouseEnabled(x=False, y=False)
        self.coronal_box.addItem(self.coronal_image)

    def init_oblique_plot(self):
        self.oblique_image = pg.ImageItem()
        self.oblique_box.setAspectLocked(True)
        self.oblique_box.showAxes(False)
        self.oblique_box.setMouseEnabled(x=False, y=False)
        self.oblique_box.addItem(self.oblique_image)