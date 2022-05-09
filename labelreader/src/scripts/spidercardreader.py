import sys

import argparse
import cv2
import pandas as pd

from pathlib import Path
#print(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent))

from ocr import tesseract


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--tesseract", required=True,
    help="path to tesseract executable")
ap.add_argument("-i", "--image", required=True,
	help="file name for and path to input image")
ap.add_argument("-l", "--language", required=False, default="eng",
    help="language that tesseract uses - depends on installed tesseract language packages")
#ap.add_argument("-c", "--codeformat", required=False, default='none', choices=['dmtx', 'qr', 'none'],
#    help="choose between searching for QR code (qr) or Data Matrix code (dmtx). Default=none - no search.")
args = vars(ap.parse_args())

print("Using language = " + args["language"] + "\n")


ocrreader = tesseract.OCR(args["tesseract"], args["language"])

ocrreader.read_image(args["image"])

ocrtext = ocrreader.get_text()
for i in range(len(ocrtext)):
    print(ocrtext[i])

ocrreader.visualize_boxes()
