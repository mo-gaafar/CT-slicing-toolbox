# CT-slicing-toolbox

This is a desktop application that can slice dicom CT series and help reconstruct view planes

## Preview Video

![CT-slicing-toolbox](preview.gif)

## Installation

```bash
git clone
cd CT-slicing-toolbox
python -m venv venv
pip install -r requirements.txt
python src/ct_toolbox.py
```

## Features

- Slice CT series

- Reconstruct view planes in:
  - Axial
  - Coronal
  - Sagittal
  - Oblique

- Measurements
  - Distance
  - Angle
  - Area