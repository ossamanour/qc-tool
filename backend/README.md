# AIAEC Siteplan Tool Project Backend

## Description

AIAEC siteplan tool development backend source code, including

1. siteplan analysis (quality control and cost estimate task) Python-based algorithm package development, and
2. Python-Flask-based backend development.

## Folder Structure

```
.
└─ 📁app        # folder containing all Python-Flask code for app
    └─ 📁blueprints # folder containing source code for API functions
    └─ 📁models     # folder containing source code related to database
    └─ __init__.py
└─ 📁dev-packages   # folder containing source code for the developed algorithm packages
└─ 📁migrations     # folder for Postgrasql database
└─ 📁server         # folder where all user files are saved on the backend server
└─ app.py           # main Python script for the backend
└─ config.py        # Python script for configure setting for the app
└─ requirements.txt # requirement file for Python virtual environment
└─ README.md        # this file
```

## Requirement

- Python 3.12
- App related packages:
  - Flask
  - flask-cors
  - Werkzeug
  - flask-sqlalchemy
  - flask-migrate
  - psycopg2
  - Flask-Session
- algorithm package related packages:

  - OpenCV \*
  - pdf2image \*
  - pytesseract \*
  - pandas
  - scikit-image
  - scikit-learn
  - requests
  - PyPDF2
  - openpyxl
  - fire
  - inquirer
  - reportlib

  \* The marked packages need special install instructions, refer to following secion **Special Python Package Install Instruction**. Other packages can be simply install by `pip` or use the `requirements.txt` file.

### Special Python Package Install Instruction

#### `OpenCV`

1. pip command to install
   ```
   pip install opencv-contrib-python
   ```

#### `pdf2image`

1. Pip command to install
   ```
   pipinstall pdf2image
   ```
2. To make the package work, `poppler` also need to be installed on the machine, follow the command listed below to install.
   ```
   sudo apt-get purge build
   sudo apt-get update
   sudo apt-get install libpoppler-dev
   sudo apt-get install poppler-utils
   ```

#### `pytesseract`

1. Pip coammnd to install
   ```
   pip install pytesseract`
   ```
2. To use the package, `tesseract` also need to be installed on the machine, follow the command listed below to install
   ```
   sudo apt update
   sudo apt install tesseract-ocr
   sudo apt install libtesseract-dev
   ```

## Environment Setup

- Development OS environment
  ```
  Ubuntu 24.04 LTS under WSL2 in Windows 11
  ```
- Create the Python Virtual Environment
  ```
  python -m venv ./venv
  ```
- Activate the Python virtual environment
  ```
  source ./venv/bin/activate
  ```
- Install necessory packages and necessory dependence. For packages need special instructions, refer to **Special Python Pacakge Install Instruction**. For other packages, install from `requirements.txt`.
  ```
  pip install -r requirements.txt
  ```
  \* Some of the requirement installation might fail, user should manually install using `pip install`.

## Usage Instruction

- Naviage to the `backend` folder, run the following command to start the backend app.

```
python app.py
```

## References

1. `tesseract` installation instruction reference: https://tesseract-ocr.github.io/tessdoc/Installation.html
2. `pytesseract` tutorial: https://github.com/NanoNets/ocr-with-tesseract/blob/master/tesseract-tutorial.ipynb
3. `opencv` document: https://docs.opencv.org/4.x/d4/da8/group__imgcodecs.html

##

Copyright (c) 2024 AIAEC, LLC All rights reserved.

Permission is NOT granted, without a fully executed written agreement with AIAEC, LLC to use, copy, modify, and/or distribute this code/data and its documentation for any purpose. If permission is granted with a fully executed written agreement, this copyright notice is required to appear in its entirety in all copies of this code/data, and in the original code/data.

IN NO EVENT SHALL AIAEC, LLC BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF THIS CODE/DATA AND ITS DOCUMENTATION, EVEN IF AIAEC, LLC HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

AIAEC, LLC DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE CODE/DATA PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND AIAEC, LLC HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS UNLESS EXPLICITLY STATED IN A FULLY EXECUTABLE AGREEMENT WITH AIAEC, LLC
