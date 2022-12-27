from PyQt5 import QtWidgets, QtCore
import numpy as np
import pyqtgraph as pg
from modules.slicevolume import get_oblique_slice
import math
from shapely import Polygon

pg.setConfigOption('imageAxisOrder', 'row-major')


class Display:
    '''
    This class initializes the all 4 pyqtgraph elements with the desired features and necessary components.
    The self.[plane]_image attribute is the element directly accessed to show/update an image.
    '''

    mw = None
    pen = pg.mkPen(color='g', width=0.5,style=QtCore.Qt.DashLine)

    selected_plot = None
    active = None
    line_start = None
    line_end = None

    poly_arr = []
    items = []

    def __init__(self, mw):
        self.mw = mw
        Display.mw = mw
        Display.init_axial_plot(self.mw)
        Display.init_sagittal_plot(self.mw)
        Display.init_coronal_plot(self.mw)
        Display.init_oblique_plot(self.mw)

        Display.selected_plot = self.mw.axial_box
        Display.active = 'polygon'

    def setActive(self, active):
        Display.active = active

        if active == 'line':
            self.line_seg = pg.LineSegmentROI([0,0], [0,0])
            self.axial_box.addItem(self.line_seg)
            Display.items.append(self.line_seg)
        elif active == 'polygon':
            self.poly = pg.PolyLineROI([[0,0], [0,0]])
            self.axial_box.addItem(self.poly)
            Display.items.append(self.poly)
        elif active == 'ellipse':
            self.ellipse = pg.EllipseROI([0,0], 0.001)
            self.axial_box.addItem(self.ellipse)
            Display.items.append(self.ellipse)


    def clear(self):
        for i in Display.items:
            self.axial_box.scene().removeItem(i)

        Display.items.clear()


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

        # self.line_seg = pg.LineSegmentROI([0,0], [0,0])
        # self.ellipse = pg.EllipseROI([0,0], 0.001)
        # self.poly = pg.PolyLineROI([[0,0], [0,0]])
        # # self.ellipse.set
        # # self.line_seg.state
        # self.axial_box.addItem(self.line_seg)
        # self.axial_box.addItem(self.ellipse)
        # self.axial_box.addItem(self.poly)
        # # self.poly.setPoints([(0,0), (200, 200), (100, 50)], True)

        self.axial_box.scene().sigMouseClicked.connect(Display.line_mouse_clicked)
        self.axial_box.scene().sigMouseClicked.connect(Display.ellipse_mouse_clicked)
        self.axial_box.scene().sigMouseClicked.connect(Display.poly_mouse_clicked)

    def line_mouse_clicked(evt):
        if Display.active == 'line':
            vb = Display.selected_plot.plotItem.vb
            scene_coords = evt.pos()
            if Display.selected_plot.sceneBoundingRect().contains(scene_coords):
                mouse_point = vb.mapSceneToView(scene_coords)

                if Display.line_start == None:
                    Display.line_start = (mouse_point.x(), mouse_point.y())
                else:
                    Display.line_end = (mouse_point.x(), mouse_point.y())
                    # line = pg.LineSegmentROI([[Display.line_start[0], Display.line_start[1]], [Display.line_end[0], Display.line_end[1]]], movable=True,rotatable=True, resizable=True)
                    # vb.addItem(line)
                    if Display.line_end:
                        handles = Display.mw.line_seg.getHandles()
                        Display.mw.line_seg.movePoint(handles[0], Display.line_start)
                        Display.mw.line_seg.movePoint(handles[1], Display.line_end)
                        length = math.dist(Display.line_start, Display.line_end)
                        Display.mw.statusbar.showMessage(f'Polygon Area: {length}')
                    Display.line_start = None
                    Display.line_end = None


    def ellipse_mouse_clicked(evt):
        if Display.active == 'ellipse':
            vb = Display.selected_plot.plotItem.vb
            scene_coords = evt.pos()
            if Display.selected_plot.sceneBoundingRect().contains(scene_coords):
                mouse_point = vb.mapSceneToView(scene_coords)

                if Display.line_start == None:
                    Display.line_start = (mouse_point.x(), mouse_point.y())
                else:
                    Display.line_end = (mouse_point.x(), mouse_point.y())
                    # line = pg.LineSegmentROI([[Display.line_start[0], Display.line_start[1]], [Display.line_end[0], Display.line_end[1]]], movable=True,rotatable=True, resizable=True)
                    # vb.addItem(line)
                    if Display.line_end:
                        Display.mw.ellipse.setPos([Display.line_start[0], Display.line_start[1]])
                        Display.mw.ellipse.setSize([Display.line_end[0] - Display.line_start[0], Display.line_end[1] - Display.line_start[1]])
                    Display.line_start = None
                    Display.line_end = None


    def poly_mouse_clicked(evt):
        if Display.active == 'polygon':
            vb = Display.selected_plot.plotItem.vb
            scene_coords = evt.pos()
            if Display.selected_plot.sceneBoundingRect().contains(scene_coords):
                mouse_point = vb.mapSceneToView(scene_coords)
                
                # Display.mw.poly.

                if len(Display.poly_arr) < 3:
                    Display.poly_arr.append((mouse_point.x(), mouse_point.y()))
                    Display.mw.poly.setPoints(Display.poly_arr, False)
                else:
                    Display.poly_arr.append((mouse_point.x(), mouse_point.y()))
                    Display.mw.poly.setPoints(Display.poly_arr, True)
                    area = Polygon(Display.poly_arr).area
                    Display.mw.statusbar.showMessage(f'Polygon Area: {area}')
                    Display.poly_arr.clear()
                    

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
        self.oblique_hline = pg.InfiniteLine(angle=0, movable=True, pen=Display.pen, name='oblique_hline')
        self.oblique_box.addItem(self.oblique_hline)

    def center_lines(self, arr):
        self.mw.axial_vline.setValue(arr.shape[1] / 2)
        self.mw.axial_hline.setValue(arr.shape[2] / 2)
        self.mw.axial_oline.setValue((arr.shape[1] / 2, arr.shape[2] / 2))

        self.mw.sagittal_vline.setValue(arr.shape[1] / 2)
        self.mw.sagittal_hline.setValue(arr.shape[0] / 2)

        self.mw.coronal_vline.setValue(arr.shape[2] / 2)
        self.mw.coronal_hline.setValue(arr.shape[0] / 2)
    

    # quick function to update the image based on axes and sync the remaining lines
    def update_image(self, arr = None, axes = None, angle = 45):
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
            # oblique moves oblique plane
            self.axial_oline.setAngle(angle)
            self.oblique_image.setImage(get_oblique_slice(arr, angle, self.axial_oline.value()))
            # print("axial oline value" + str(self.axial_oline.value()))
            # print("axial oline angle" + str(self.axial_oline.angle()))
        
        elif axes == 'coronal':
            # update lines in other planes
            # vertical moves vertical in axial plane
            self.axial_vline.setValue(self.coronal_vline.value())
            # horizontal moves horizontal in sagittal plane
            self.sagittal_hline.setValue(self.coronal_hline.value())
            # horizontal moves horizontal in oblique plane
            self.oblique_hline.setValue(self.coronal_hline.value())

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
            # horizontal moves horizontal in oblique plane
            self.oblique_hline.setValue(self.sagittal_hline.value())

            # update slices in other planes
            # horizontal moves axial plane
            self.axial_image.setImage(arr[int(self.sagittal_hline.value()), :, :])
            # vertical moves coronal plane
            self.coronal_image.setImage(arr[:, int(self.sagittal_vline.value()), :])

        elif axes == 'oblique':
            # update lines in other planes
            # horizontal moves horizontal in coronal plane
            self.coronal_hline.setValue(self.oblique_hline.value())
            # horizontal moves horizontal in sagittal plane
            self.sagittal_hline.setValue(self.oblique_hline.value())
            
            # update slices in other planes
            # horizontal moves axial plane
            self.axial_image.setImage(arr[int(self.oblique_hline.value()), :, :])


        