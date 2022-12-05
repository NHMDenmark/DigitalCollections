import argparse
import pandas as pd



# Remember to run this command line first to convert to UTF8 format:
# iconv -f ISO-8859-1 -t UTF-8 Naturalis-image-file_opdateret2.csv > Naturalis-image-file_opdateret2_utf8.csv


def main():
    """The main function of this script."""

    #infilename = "../Naturalis-image-file_utf8.csv"
    #outfilename = "../Naturalis-image-file_utf8_fixed.csv"
    infilename = "../Naturalis-image-file_opdateret2_utf8.csv"
    outfilename = "../Naturalis-image-file_opdateret2_utf8_fixed.csv"

    table = pd.read_csv(infilename, sep=';')
    
    # Rename this column
    #table = table.rename(columns={"taxon_id_at_source": "taxon_id_at_source_short"})
    #table = table.rename(columns={"taxon_id_at_source2": "taxon_id_at_source"})

    # Add missing columns
    table["morph"] = ""
    table["morph_id"] = ""
    table["rijkdriehoeksstelsel_x"] = ""
    table["rijkdriehoeksstelsel_y"] = ""
    
    
    # Write to CSV file using comma separator 
    table.to_csv(outfilename, index=False, sep=',')


if __name__ == '__main__':
    main()


