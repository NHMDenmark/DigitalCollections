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
parser.add_argument('--output', help='path to a directory to write a CSV file with the sampled records and downloaded images to', default='.')
parser.add_argument('--samples', help='set number of randomly picked rows from the CSV file', type=int, default=10)
parser.add_argument('--df', help='downsampling factor to be applied to images prior to writing to disk', type=float, default=1.0)
parser.add_argument('--Q', help='set the JPEG quality parameter for processed images', type=int, default=50)
args = parser.parse_args()


# EXAMPLE:
# python herbariumdownloader.py --input /Users/kimstp/Documents/NHMD/data/Herbarium/query_results_23032022.csv --samples 10 --df 0.5 --output /Users/kimstp/Dropbox/NHMD/Herbarium/Natalie

# python herbariumdownloader.py --input /Users/kimstp/Documents/NHMD/data/Herbarium/query_results_23032022.csv --samples 100 --df 0.5 --output /Users/kimstp/Dropbox/NHMD/Herbarium/Natalie


# TODO: Add check for validity of args.input string
sheet=pd.read_csv(PurePath(args.input), low_memory=False) # Read CSV file


# Pick randomly some rows out of the dataframe
subsheet = sheet.sample(n=args.samples)


# Write the selected records to a CSV file
subsheet.to_csv(PurePath(args.output, 'samples.csv'), index=False)

# Walk through sampled records and download images, downsample and save to disk
for index, record in subsheet.iterrows():
    # TODO: Handle that some records may have multiple attachments separated by ';'
    url = record["1,111-collectionobjectattachments.collectionobject.collectionObjectAttachments"]
    catnum = record["1.collectionobject.catalogNumber"]
    print("Catalogue number NHMD-" + str(catnum))
    print("Download " + url)
    try:
        # TODO: Make a urllib.request based downloader instead of assuming wget is installed in the OS
        # Set the download path to be identical to the output path
        retval = subprocess.run(["wget -P" + PurePath(args.output).as_posix() + " " + str(url)], shell=True, check=True)
        #print(retval)
        
        # Read image, downsample and write back to disk using NHMD catalogue number as file name. Set JPEG compression factor
        imgfilename = PurePath(urlparse(url).path).name # Strip filename from URL
        img = imread(PurePath(args.output,imgfilename).as_posix())
        
        # Downsample by a factor of args.df using nearest neighbor interpolation and anti aliasing by Gaussian filtering prior to sampling
        imgrescaled = img_as_ubyte(rescale(img, args.df, order=0, multichannel=True, anti_aliasing=True))
        
        # Set output file name to NHMD catalogue number
        outfilename = "NHMD-" + str(catnum) + ".jpg"
        print("Saving image " + outfilename)
        imsave(PurePath(args.output, outfilename).as_posix(), imgrescaled, quality=args.Q)
        
        # TODO: Delete the original downloaded file
        
        
    except subprocess.CalledProcessError as e:
        print("Download failed - skipping this image")
        print(e)

