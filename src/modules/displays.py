from PyQt5 import QtWidgets, QtCore
import numpy as np
import pyqtgraph as pg


pg.setConfigOption('imageAxisOrder', 'row-major')


class Display:
    '''
    This class initializes the all 4 pyqtgraph elements with the desired features and necessary components.
    The self.[plane]_image attribute is the element directly accessed to show/update an image.
    '''

    mw = None
    pen = pg.mkPen(color='g', width=0.5,style=QtCore.Qt.DashLine)

    def __init__(self, mw):
        self.mw = mw
        Display.init_axial_plot(self.mw)
        Display.init_sagittal_plot(self.mw)
        Display.init_coronal_plot(self.mw)
        Display.init_oblique_plot(self.mw)


    def init_axial_plot(self):
        self.axial_image = pg.ImageItem()
        
        self.axial_box.setAspectLocked(True)
        self.axial_box.showAxes(False)
        self.axial_box.setMouseEnabled(x=False, y=False)
        self.axial_box.addItem(self.axial_image)

        self.axial_vline = pg.InfiniteLine(angle=90, movable=True, pen=Display.pen, name='axial_vline')
        self.axial_hline = pg.InfiniteLine(angle=0, movable=True, pen=Display.pen, name='axial_hline')
        self.axial_oline = pg.InfiniteLine(angle=135, movable=True, pen=Display.pen, name='axial_oline')
        self.axial_box.addItem(self.axial_vline)
        self.axial_box.addItem(self.axial_hline)
        self.axial_box.addItem(self.axial_oline)

    def init_sagittal_plot(self):
        self.sagittal_image = pg.ImageItem()

        self.sagittal_box.setAspectLocked(True)
        self.sagittal_box.showAxes(False)
        self.sagittal_box.setMouseEnabled(x=False, y=False)
        self.sagittal_box.addItem(self.sagittal_image)

        self.sagittal_vline = pg.InfiniteLine(angle=90, movable=True, pen=Display.pen, name='sagittal_vline')
        self.sagittal_hline = pg.InfiniteLine(angle=0, movable=True, pen=Display.pen, name='sagittal_hline')
        self.sagittal_box.addItem(self.sagittal_vline)
        self.sagittal_box.addItem(self.sagittal_hline)

    def init_coronal_plot(self):
        self.coronal_image = pg.ImageItem()

        self.coronal_box.setAspectLocked(True)
        self.coronal_box.showAxes(False)
        self.coronal_box.setMouseEnabled(x=False, y=False)
        self.coronal_box.addItem(self.coronal_image)

        self.coronal_vline = pg.InfiniteLine(angle=90, movable=True, pen=Display.pen, name='coronal_vline')
        self.coronal_hline = pg.InfiniteLine(angle=0, movable=True, pen=Display.pen, name='coronal_hline')
        self.coronal_box.addItem(self.coronal_vline)
        self.coronal_box.addItem(self.coronal_hline)

    def init_oblique_plot(self):
        self.oblique_image = pg.ImageItem()
        self.oblique_box.setAspectLocked(True)
        self.oblique_box.showAxes(False)
        self.oblique_box.setMouseEnabled(x=False, y=False)
        self.oblique_box.addItem(self.oblique_image)

    def center_lines(self, arr):
        self.mw.axial_vline.setValue(arr.shape[1] / 2)
        self.mw.axial_hline.setValue(arr.shape[2] / 2)
        self.mw.axial_oline.setValue((arr.shape[1] / 2, arr.shape[2] / 2))

        self.mw.sagittal_vline.setValue(arr.shape[1] / 2)
        self.mw.sagittal_hline.setValue(arr.shape[0] / 2)

        self.mw.coronal_vline.setValue(arr.shape[2] / 2)
        self.mw.coronal_hline.setValue(arr.shape[0] / 2)
    

    # quick function to update the image based on axes and sync the remaining lines
    def update_image(self, arr = None, axes = None):
        if arr is None:
            print("No array passed to update_image")
            return
        if axes == 'axial':
            # update lines in other planes
            # vertical moves vertical in coronal plane
            self.coronal_vline.setValue(self.axial_vline.value())
            # horizontal moves vertical in sagittal plane
            self.sagittal_vline.setValue(self.axial_hline.value())

            # update slices in other planes
            #vertical moves sagittal plane
            self.sagittal_image.setImage(arr[:, :, int(self.axial_vline.value())])
            #horizontal moves coronal plane
            self.coronal_image.setImage(arr[:, int(self.axial_hline.value()), :])
        
        elif axes == 'coronal':
            # update lines in other planes
            # vertical moves vertical in axial plane
            self.axial_vline.setValue(self.coronal_vline.value())
            # horizontal moves horizontal in sagittal plane
            self.sagittal_hline.setValue(self.coronal_hline.value())

            # update slices in other planes
            # horizontal moves axial plane
            self.axial_image.setImage(arr[int(self.coronal_hline.value()), :, :])
            # vertical moves sagittal plane
            self.sagittal_image.setImage(arr[:, :, int(self.coronal_vline.value())])
        
        elif axes == 'sagittal':
            # update lines in other planes
            # vertical moves horizontal in axial plane
            self.axial_hline.setValue(self.sagittal_vline.value())
            # horizontal moves horizontal in coronal plane
            self.coronal_hline.setValue(self.sagittal_hline.value())

            # update slices in other planes
            # horizontal moves axial plane
            self.axial_image.setImage(arr[int(self.sagittal_hline.value()), :, :])
            # vertical moves coronal plane
            self.coronal_image.setImage(arr[:, int(self.sagittal_vline.value()), :])