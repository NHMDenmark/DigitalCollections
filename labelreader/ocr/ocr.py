import pytesseract
import pandas as pd


class OCR():
    """This class is a wrapper on the tesseract and pytesseract OCR library.
    """
    
    def __init__(self, tesseract_cmd, language):
        """        
        tesseract_cmd - must be set to the path to the tesseract executable
        language - String setting the language to use by tesseract. Multi-languages can be defined as e.g. 'eng+dan' """
        pytesseract.tesseract_cmd = tesseract_cmd
        self._language = language
        self.ocr_result = None
    
    
    
    def read_image(self, image):
        """Parses the image and populates the internal data structures of this class"""
        self.ocr_result = pytesseract.image_to_data(image, lang=self._language, output_type=pytesseract.Output.DATAFRAME)
        
    def get_text(self):
        """Returns a list of the read text. Remember to call read_image before calling this method."""
        retlist = []
        if self.ocr_result == None:
            print("Warning: You must call read_image prior to calling the get_text method!")
        else:
            for index, row in self.ocr_result.iterrows():
                if row['conf'] > 0:
                    retlist.append(row['text'])
                    
        return retlist
