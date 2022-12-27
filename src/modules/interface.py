
# from turtle import onrelease
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import *
from modules.displays import Display
from modules.utility import print_debug
from modules import browse


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
    
    self.axial_vline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"axial", self.angle_slider.value()))
    self.axial_hline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"axial", self.angle_slider.value()))
    self.axial_oline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"axial", self.angle_slider.value()))

    self.sagittal_vline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"sagittal"))
    self.sagittal_hline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"sagittal"))

    self.coronal_vline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"coronal"))
    self.coronal_hline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"coronal"))

    self.oblique_hline.sigPositionChanged.connect(lambda: Display.update_image(self, self.volume_array,"oblique"))
    
    self.angle_slider.valueChanged.connect(lambda: Display.update_image(self, self.volume_array,"axial", self.angle_slider.value()))
    # self.angle_slider.valueChanged.connect(lambda: axial_oline.set)
    self.angle_slider.valueChanged.connect(lambda: self.angle_label.setText(str("Anlge: "+str(self.angle_slider.value()))))
    self.line.clicked.connect(
        lambda: Display.setActive(self, 'line')
    )
    self.polygon.clicked.connect(
        lambda: Display.setActive(self, 'polygon')
    )
    self.elps.clicked.connect(
        lambda: Display.setActive(self, 'ellipse')
    )
    self.angle.clicked.connect(
        lambda: Display.setActive(self, 'angle')
    )
    self.clear.clicked.connect(
        lambda: Display.clear(self)
    )
    
    print_debug("Connectors Initialized")

def about_us(self):
    QMessageBox.about(
        self, ' About ', 'This is a Medical Image Viewer \nCreated by junior students from the faculty of Engineering, Cairo Uniersity, Systems and Biomedical Engineering department \n \n Created By: Mohamed Nasser ')
