from PyQt5.QtWidgets import QFileDialog
import SimpleITK as sitk
import matplotlib.pyplot as plt
import math
from modules.displays import Display


def browse_window(self):

    self.directory = QFileDialog.getExistingDirectory(
        None, 'open the desired directory', './')
    
    print(self.directory)

    volume_array = importer(self, self.directory)

    # Move lines to be centered with image
    self.disp.center_lines(volume_array)

    # Display samples of all three planes from the 3d volume_array
    self.axial_image.setImage(volume_array[100, :, :])
    self.coronal_image.setImage(volume_array[:, 270, :])
    self.sagittal_image.setImage(volume_array[:, :, 270])

    self.volume_array = volume_array 


def importer(self, path):
    # Initialize itk reader
    reader = sitk.ImageSeriesReader()

    # Read all file names in given directory
    dicom_names = reader.GetGDCMSeriesFileNames(path)

    # Set these filenames in the itk reader
    reader.SetFileNames(dicom_names)

    # Execute the reader --> automatically uses the data in all the files to create a 3d volume
    image = reader.Execute()
    # print
    Display.init_resampler(self, image)

    # resampler = sitk.ResampleImageFilter()
    # resampler.SetReferenceImage(image)

    # width, height, depth = image.GetSize()
    # center = image.TransformIndexToPhysicalPoint((int(math.ceil(width/2)),
    #                                       int(math.ceil(height/2)),
    #                                       int(math.ceil(depth/2))))

    # transform = sitk.GridImageSource()
    # transform.SetSize()
    # transform = sitk.Euler3DTransform(center, math.radians(170))
    # resampler.SetInterpolator(sitk.sitkNearestNeighbor)
    # resampler.SetTransform(transform)
    # # resampler.SetOutputDirection((1, 0, 0, ))
    # out = resampler.Execute(image)
    # out = sitk.GetArrayFromImage(out)
    # plt.imshow(out[200, :, :])
    # plt.show()
    
    # reader.

    # Extract 3d np array from itk 3d volume
    image_array = sitk.GetArrayFromImage(image)

    return image_array