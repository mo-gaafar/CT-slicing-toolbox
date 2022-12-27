from dataclasses import dataclass, field
import numpy as np
import scipy

@dataclass
class SliceVolume:
    '''SliceVolume is a class that can be used to slice a volume along 4 axes.

    The class is initialized with a np.ndarray volume.'''

    volume: np.ndarray = field(init=True)
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

#TODO: to be integrated into class later
def get_oblique_slice(arr, angle, point):
            # slice through an array given a point and angle of a line in y,z plane
            # point is a tuple of (y,z) coordinates
            # angle is in degrees
            # returns a 2d array of the slice

            # convert angle to radians
            angle = angle * np.pi / 180

            # get the slope of the line from angle
            slope = np.tan(angle)

            if type(point) == list:
                y = point[1]
                z = point[0]
            elif angle - np.pi/2 < 0.01:
                y = 0
                z = point
            elif angle == np.pi:
                y = point
                z = 0
                
            # point on the line that is closest to the origin
            # this is the point where the line crosses the y axis
            y0 = y - slope * z

            # z intercept of the line
            z0 = z - y / slope

            # get an array of discrete coordinates along the line in 3d space 
            # this is the line that will be sliced through the array
            slice = np.zeros((arr.shape[1], arr.shape[2]))

            #intersection with boundary
            zb = (arr.shape[1] - y0) / slope

            # clip the line intercepts to the boundaries of the array
            if zb >= arr.shape[2]:
                zb = arr.shape[2]-1
            if zb < 0:
                zb = 0
                
            if z0 >= arr.shape[2]:
                z0 = arr.shape[2]-1
            if z0 < 0:
                z0 = 0

            # generate linespace of z coordinates dependent on array size
            # check if z0 or zb are NaN
            if np.isnan(z0):
                z0 = 0
            if np.isnan(zb):
                zb = arr.shape[2]-1
                
            z_coords = np.linspace(int(z0),int(zb)-1, arr.shape[2])
            y_coords = z_coords * slope + y0
            
            for i in range(len(y_coords)):
                y = int(round(y_coords[i]))
                if y < 0 or y>= arr.shape[1]:
                    y_coords[i] = 0

            z_coords = np.round(z_coords)

            # get the pixels on the plane in x axis
            plane = arr[ :, y_coords.astype(int), z_coords.astype(int)]
            # make the plane a 2d array
            plane = np.squeeze(plane)
            
            return plane
