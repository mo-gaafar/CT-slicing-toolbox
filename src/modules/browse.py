from PyQt5.QtWidgets import QFileDialog
import SimpleITK as sitk


def browse_window(self):

    self.directory = QFileDialog.getExistingDirectory(
        None, 'open the desired directory', './')
    
    print(self.directory)

    volume_array = importer(self.directory)

    # Move lines to be centered with image
    self.disp.center_lines(volume_array)

    # Display samples of all three planes from the 3d volume_array
    self.axial_image.setImage(volume_array[100, :, :])
    self.coronal_image.setImage(volume_array[:, 270, :])
    self.sagittal_image.setImage(volume_array[:, :, 270])

    self.volume_array = volume_array 


def importer(path):
    # Initialize itk reader
    reader = sitk.ImageSeriesReader()

    # Read all file names in given directory
    dicom_names = reader.GetGDCMSeriesFileNames(path)

    # Set these filenames in the itk reader
    reader.SetFileNames(dicom_names)

    # Execute the reader --> automatically uses the data in all the files to create a 3d volume
    image = reader.Execute()

    # Extract 3d np array from itk 3d volume
    image_array = sitk.GetArrayFromImage(image)

    return image_array