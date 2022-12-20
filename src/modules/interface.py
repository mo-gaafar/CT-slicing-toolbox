
# from turtle import onrelease
from PyQt5.QtWidgets import QTabWidget, QAction, QPushButton, QSlider, QComboBox, QLCDNumber, QMessageBox
from PyQt5.QtGui import *
# import numpy as np
# from PIL import Image as PILImage
# from PyQt5 import QtGui
# import os
from modules.displays import Display
from modules.utility import print_debug
from modules import browse



# def refresh_display(self):
#     ''' Updates the user interface with the current image and data'''
#     #TODO update output image here
#     display_pixmap(self, image_data=self.image1.get_pixels())

#     #TODO update metadata here
#     display_list(self)

# def display_pixmap(self, image_data):
#     '''Displays the image data in the image display area'''
#     # then convert it to image format
#     data = PILImage.fromarray(image_data.astype(np.uint8))
#     # save the image file as png
#     data.save('temp.png')
#     # display saved image in Qpixmap
#     self.image1_widget.setPixmap(QtGui.QPixmap("temp.png"))
#     self.image1_widget.show()
#     # delete the temporary image file
#     os.remove('temp.png')


# def display_list(self):
#     '''Displays the metadata in qlabel'''
#     f_metadata = self.image1.get_formatted_metadata()
#     self.metadata_widget.setText(f_metadata)


def init_connectors(self):
    '''Initializes all event connectors and triggers'''

    # ''' Menu Bar'''

    # self.actionAbout_Us = self.findChild(QAction, "actionAbout_Us")
    # self.actionAbout_Us.triggered.connect(
    #     lambda: about_us(self))

    # self.WindowTabs = self.findChild(QTabWidget, "WindowTabs")

    ''' Browse buttons'''
    # the index argument maps each function to its respective slot
    self.actionOpen.triggered.connect(
        lambda: browse.browse_window(self))

    # connectors to the pyqtgraph lines
    # useful docs: https://pyqtgraph.readthedocs.io/en/latest/api_reference/graphicsItems/infiniteline.html#pyqtgraph.InfiniteLine
    #connect lines to sigPositionChanged event
    
    self.volume_array = None
    
    self.axial_vline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"axial"))
    self.axial_hline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"axial"))
    self.axial_oline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"axial", self.angle_slider.value()))

    self.sagittal_vline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"sagittal"))
    self.sagittal_hline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"sagittal"))

    self.coronal_vline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"coronal"))
    self.coronal_hline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"coronal"))

    self.oblique_hline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"oblique"))
    
    self.angle_slider.valueChanged.connect(lambda: Display.update_image(self, self.volume_array,"axial", self.angle_slider.value()))
    # self.angle_slider.valueChanged.connect(lambda: axial_oline.set)
    self.angle_slider.valueChanged.connect(lambda: self.angle_label.setText(str("Anlge: "+str(self.angle_slider.value()))))
    
    print_debug("Connectors Initialized")

def about_us(self):
    QMessageBox.about(
        self, ' About ', 'This is a Medical Image Viewer \nCreated by junior students from the faculty of Engineering, Cairo Uniersity, Systems and Biomedical Engineering department \n \n Created By: Mohamed Nasser ')
