import argparse
import pandas as pd


parser = argparse.ArgumentParser(description='Process a CSV file and download images listed in it.')
parser.add_argument('--input', help='path to the input CSV file')
parser.add_argument('--output', help='path to a directory to write the downloaded images to', default='')
parser.add_argument('--samples', help='set number of randomly picked rows from the CSV file', default=1)
parser.add_argument('--df', help='downsampling factor to be applied to images prior to writing to disk', default=1.0)
args = parser.parse_args()


# TODO: Add check for validity of args.input string
sheet=pd.read_csv(args.input) # Read CSV file



# Pick randomly some rows out of the dataframe
subsheet = sheet.sample(n=args.samples)


# Write the selected records to a CSV file
subsheet.to_csv(args.output + 'test.csv', index=False)


