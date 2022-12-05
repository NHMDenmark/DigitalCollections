import argparse
import pandas as pd


# Remember to run this command line first to convert to UTF8 format:
# iconv -f ISO-8859-1 -t UTF-8 Naturalis-taxa-file_opdateret2.csv > Naturalis-taxa-file_opdateret2_utf8.csv




def main():
    """The main function of this script."""

    #infilename = "../Naturalis-taxa-file_utf8.csv"
    #outfilename = "../Naturalis-taxa-file_utf8_fixed.csv"
    infilename = "../Naturalis-taxa-file_opdateret2_utf8.csv"
    outfilename = "../Naturalis-taxa-file_opdateret2_utf8_fixed.csv"

    # Read file
    table = pd.read_csv(infilename, sep=';') 
    
    # Rename this column
    table = table.rename(columns={"phylum": "division"}) 
    
    # Fix status_at_source from Accepted -> accepted and Synonym -> synonym
    table["status_at_source"] = table["status_at_source"].str.lower()
        
    # Write to CSV file using comma separator 
    table.to_csv(outfilename, index=False, sep=',') 


if __name__ == '__main__':
    main()


