from dataclasses import dataclass, field
import numpy as np
import scipy

@dataclass
class SliceVolume:
    '''SliceVolume is a class that can be used to slice a volume along 4 axes.

    The class is initialized with a np.ndarray volume.'''

    volume: np.ndarray = field(required=True)
    axial: np.ndarray = field(init=False)
    sagittal: np.ndarray = field(init=False)
    coronal: np.ndarray = field(init=False)
    oblique: np.ndarray = field(init=False)

    def __post_init__(self):
        self.axial = self.volume[np.size(self.volume)[0]//2, :, :]
        self.sagittal = self.volume[:, 0, :]
        self.coronal = self.volume[:, :, 0]
        self.oblique = None

    def slice_axial(self, slice_number):
        self.axial = self.volume[slice_number, :, :]
    
    def slice_sagittal(self, slice_number):
        self.sagittal = self.volume[:, slice_number, :]
    
    def slice_coronal(self, slice_number):
        self.coronal = self.volume[:, :, slice_number]

    # slice oblique takes a plane in 3d space and slices the volume along that plane
    def slice_oblique(self, plane):
        # get coordinates along the plane
        x, y, z = np.where(plane)
        # get the coordinates of the volume
        x_v, y_v, z_v = np.indices(self.volume.shape)
        # get the coordinates of the volume that are on the plane
        x_v = x_v[plane]
        y_v = y_v[plane]
        z_v = z_v[plane]
        # get the values of the volume that are on the plane
        values = self.volume[plane]
        # interpolate the values of the volume at the coordinates of the plane
        self.oblique = scipy.interpolate.griddata((x_v, y_v, z_v), values, (x, y, z), method='linear')


