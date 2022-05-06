# HerbariumLabels
Experimenting with automated reading of Herbarium labels.

Python scripts and ideas for automated reading of machine typed labels (not yet handwritten labels) and Data Matric codes or QR codes.

## Requirements
The following must be installed on the system. On MacOS I install via MacPorts.
```sh
tesseract
tesseract-dan
tesseract-eng
zbar
libdmtx
```

Create virtual environment
```sh
python3 -m venv venv
```

Install via pip into virtual environment
```sh
source venv/bin/activate
pip install --upgrade pip
pip install opencv-contrib-python 
pip install pytesseract
pip install pyzbar
pip install pylibdmtx
```
or simply
```sh
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```


## Kims notes
POStagger, Named Entity, Language detector, and a lot of other stuff - Polyglot:
https://github.com/aboSamoor/polyglot

DanNLP:
https://github.com/alexandrainst/danlp
