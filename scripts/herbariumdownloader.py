import argparse
import subprocess
from urllib.parse import urlparse
from pathlib import PurePath
import pandas as pd
from skimage.io import imread, imsave 
from skimage.transform import rescale
from skimage.util import img_as_ubyte

# Command-line argument parsing
parser = argparse.ArgumentParser(description='Randomly sample records from a CSV file and download images listed in it.')
parser.add_argument('--input', help='path to the input CSV file')
parser.add_argument('--output', help='path to a directory to write a CSV file with the sampled records and downloaded images to', default='')
parser.add_argument('--samples', help='set number of randomly picked rows from the CSV file', type=int, default=10)
parser.add_argument('--df', help='downsampling factor to be applied to images prior to writing to disk', type=float, default=1.0)
args = parser.parse_args()


# TODO: Add check for validity of args.input string
sheet=pd.read_csv(args.input, low_memory=False) # Read CSV file


# Pick randomly some rows out of the dataframe
subsheet = sheet.sample(n=args.samples)


# Write the selected records to a CSV file
subsheet.to_csv(PurePath(args.output, 'samples.csv'), index=False)

# Walk through sampled records and download images, downsample and save to disk
for url in subsheet["1,111-collectionobjectattachments.collectionobject.collectionObjectAttachments"]:
    print("Download " + url)
    try:
        # TODO: Make a urllib.request based downloader instead of assuming wget is installed in the OS
        retval = subprocess.run(["wget " + str(url)], shell=True, check=True)
        #print(retval)
        
        # Read image, downsample and write back to disk using NHMD catalogue number as file name. Set JPEG compression factor
        imgfilename = PurePath(urlparse(url).path).name
        img = imread(imgfilename)
        
        imgrescaled = rescale(img, args.df, order=1, multichannel=True, anti_aliasing= True)
        
        # TODO Set output file name to NHMD catalogue number
        imsave(PurePath(args.output, 'samples.jpg').as_posix(), img_as_ubyte(imgrescaled), quality=50)
        
        
    except subprocess.CalledProcessError as e:
        print("Download failed - skipping this image")
        print(e)

