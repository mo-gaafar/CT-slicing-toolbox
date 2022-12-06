from dataclasses import dataclass, field
import numpy as np
from abc import ABC
import pyqtgraph as pg


@dataclass
class PlotWindow(ABC):
    '''This is a class that contains all information about a plot window.'''
    
    mw_ref: object = field(default=None, required=True)
    plotw_ref: object = field(default=None, required=True)
    # vol_ref: object = field(default=None, required=True)

    plane_name: str = field(default='undefined')
    plane_data: np.ndarray = field(default=None)
    slicing_lines_data: dict = field(default=None)
    slicing_lines_ref: dict = field(default=None)
    measurement_objects_dict: dict = field(default_factory=dict)
    scale_conversion_factor: tuple = field(default=(1, 1))
    scale_conversion_factor_unit: tuple = field(default=('mm', 'mm'))

    def init_ui(self):
        """This method initializes the ui of the plot window"""
        # takes pyqtgraph plot widget as input
        if self.plotw_ref is None:
            raise ValueError('No pyqtgraph plot widget found')

        # creates a dict of slicing lines from slicing lines data
        self.slicing_lines_ref = self.create_slicing_lines_ref()

        # takes the line ref dict as input
        for name, line_ref in self.slicing_lines_ref:
            # add to pg plot
            self.plotw_ref.addItem(line_ref, label = name)

    def create_slicing_lines_ref(self):
        """This method creates a dict of slicing lines from slicing lines data"""
        # create an empty dict
        slicing_lines_ref = {}
        # loop over the slicing lines data
        for name, line_data in self.slicing_lines_data:
            # create a pyqtgraph line from the line data
            line_ref = self.from_np_line(line_data)
            # add the line to the dict
            slicing_lines_ref[name] = line_ref
        # return the dict
        return slicing_lines_ref

    def from_pg_line(self, pg_line):
        """Converts a pyqtgraph line to a np line"""

        # get the line data
        line_data = pg_line.getData()
        # convert the line data to a numpy array
        line_data = np.array(line_data)
        # transpose the line data
        line_data = line_data.T
        # return the line data
        return line_data
    
    def from_np_line(self, np_line):
        """Converts a numpy line to a pyqtgraph line"""
        # transpose the line data
        np_line = np_line.T
        # convert the line data to a list
        np_line = np_line.tolist()
        # create a pyqtgraph line from the line data
        pg_line = pg.PlotDataItem(np_line)
        # return the line
        return pg_line

    def get_plane_data(self):
        return self.plane_data
    
    def get_measurements(self):
        return self.measurement_objects_dict
    
    def get_slicing_line(self):
        return self.slicing_line
    
    def add_measurement(self, measurement_object):
        self.measurement_objects_dict[measurement_object.name] = measurement_object
    
    def remove_measurement(self, measurement_object):
        del self.measurement_objects_dict[measurement_object.name]
    
class AxialPlotWindow(PlotWindow):
    def __init__(self):
        super().__init__()
        self.plane_name = 'axial'
        self.slicing_lines_data = {'vertical': np.array([[0, 0], [0, 0]]),
                                   'horizontal': np.array([[0, 0], [0, 0]]),
                                   'oblique': np.array([[0, 0], [0, 0]])}
        self.init_ui()

class SagittalPlotWindow(PlotWindow):
    def __init__(self):
        super().__init__()
        self.plane_name = 'sagittal'
        self.slicing_lines_data = {'vertical': np.array([[0, 0], [0, 0]]),
                                    'horizontal': np.array([[0, 0], [0, 0]])}
        self.init_ui()
    
class CoronalPlotWindow(PlotWindow):
    def __init__(self):
        super().__init__()
        self.plane_name = 'coronal'
        self.slicing_lines_data = {'vertical': np.array([[0, 0], [0, 0]]),
                                    'horizontal': np.array([[0, 0], [0, 0]])}
        self.init_ui()

class ObliquePlotWindow(PlotWindow):
    def __init__(self):
        super().__init__()
        self.plane_name = 'oblique'
        self.slicing_lines_data = {'vertical': np.array([[0, 0], [0, 0]]),
                                    'horizontal': np.array([[0, 0], [0, 0]])}
        self.init_ui()

    
@dataclass
class PlotWindows:
    """This class contains all plot windows.
    Contains window synchronization logic
    """
    mw_ref: object = field(default=None, required=True)

    axial: PlotWindow = field(default_factory=PlotWindow)
    sagittal: PlotWindow = field(default_factory=PlotWindow)
    coronal: PlotWindow = field(default_factory=PlotWindow)
    oblique: PlotWindow = field(default_factory=PlotWindow)

    def __post_init__(self):
        self.axial = AxialPlotWindow(self.mw_ref)
        self.sagittal = SagittalPlotWindow(self.mw_ref)
        self.coronal = CoronalPlotWindow(self.mw_ref)
        self.oblique = ObliquePlotWindow(self.mw_ref)

    def sync_lines(self, triggering_window):
        """#TODO: Syncs the slicing lines between the plot windows"""
        # get the slicing line from the triggering window
        #NOTE: visualize slicing planes in 3d space for easier understanding
        pass

    def update_plane_data(self):
        """#TODO: Updates the plane data of all plot windows, using the line data of the windows after syncing"""
        pass
    
    def get_axial(self):
        return self.axial
    
    def get_sagittal(self):
        return self.sagittal
    
    def get_coronal(self):
        return self.coronal
    
    def get_oblique(self):
        return self.oblique

    
