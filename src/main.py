import SimpleITK as sitk
import matplotlib.pyplot as plt

plt.rcParams["figure.autolayout"] = True

# Initialize itk reader
reader = sitk.ImageSeriesReader()

# Read all file names in given directory
dicom_names = reader.GetGDCMSeriesFileNames('datasets\Head')

# Set these filenames in the itk reader
reader.SetFileNames(dicom_names)

# Execute the reader --> automatically uses the data in all the files to create a 3d volume
image = reader.Execute()

# Extract 3d np array from itk 3d volume
image_array = sitk.GetArrayFromImage(image)

# Create 3 subplots
fig, axs = plt.subplots(3)
print(image_array.shape)

# Loop over the three axes and plot them simultaneously in their plots
for i in range(image.GetSize()[2]):
    plt.axes(axs[0])
    plt.imshow(image_array[i, :, :], cmap='gray')

    plt.axes(axs[1])
    plt.imshow(image_array[:, i+image.GetSize()[2]//2, :], cmap='gray')

    plt.axes(axs[2])
    plt.imshow(image_array[:, :, i+image.GetSize()[2]//2], cmap='gray')

    plt.draw()
    plt.pause(0.00000000001)
    plt.clf()