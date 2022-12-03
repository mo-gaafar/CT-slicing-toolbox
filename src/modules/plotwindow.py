from dataclasses import dataclass, field
import numpy as np


@dataclass
class PlotWindow:
    '''This is a class that contains all information about a plot window.'''
    
    plane_name: str = field(default='axial')
    plane_data: np.ndarray = field(default=None)
    slicing_line: np.ndarray = field(default=None)
    measurement_objects_dict: dict = field(default_factory=dict)
    scale_conversion_factor: tuple = field(default=(1, 1))
    scale_conversion_factor_unit: tuple = field(default=('mm', 'mm'))

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
    


@dataclass
class PlotWindows:
    """This class contains all plot windows."""
        
        axial: PlotWindow = field(default_factory=PlotWindow)
        sagittal: PlotWindow = field(default_factory=PlotWindow)
        coronal: PlotWindow = field(default_factory=PlotWindow)
        oblique: PlotWindow = field(default_factory=PlotWindow)
        
        def get_axial(self):
            return self.axial
        
        def get_sagittal(self):
            return self.sagittal
        
        def get_coronal(self):
            return self.coronal
        
        def get_oblique(self):
            return self.oblique

            
