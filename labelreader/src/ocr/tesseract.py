import pytesseract
import pandas as pd
import cv2



class OCR():
    """This class is a wrapper data structure on the tesseract and pytesseract OCR library.
    """
    
    def __init__(self, tesseract_cmd, language):
        """        
        tesseract_cmd - must be set to the path to the tesseract executable
        language - String setting the language to use by tesseract. Multi-languages can be defined as e.g. 'eng+dan' """
        self._tesseract_cmd = tesseract_cmd
        pytesseract.tesseract_cmd = self._tesseract_cmd
        self._language = language
        self.ocr_result = None
    
    
    def read_image(self, image):
        """Parses the image and populates the internal data structures of this class.
        The image must be a numpy array in RGB color channel order."""
        self.image = image
        self.ocr_result = pytesseract.image_to_data(image, lang=self._language, output_type=pytesseract.Output.DATAFRAME)
        
        
    def get_text(self):
        """Returns a list of strings with the text read from the image. 
        
        Remember to call read_image before calling this method."""
        retlist = []
        if isinstance(self.ocr_result, type(None)):
            print("Warning: You must call read_image prior to calling the get_text method!")
        else:
            linenum = 0
            linetext = []
            # Make a sentence of read symbols for each line read in the image
            for index, row in self.ocr_result.iterrows():
                if row['conf'] > 0 and row['width'] * row['height'] > 10: # Check confidence value and that the box has area larger than 10 pixels^2
                    #if row['line_num'] != linenum and row['word_num'] == 1:
                    if row['word_num'] == 1:
                        if len(linetext) != 0:
                            retlist.append(linetext)
                            
                        linetext = []
                        linenum = row['line_num']
                        
                    linetext.append(row['text'])
            
            if len(linetext) != 0:
                retlist.append(linetext)
                    
        return retlist

    def visualize_boxes(self):
        """Visualize the blocks of text detected by tesseract.
        
        Remember to call read_image before calling this method.
        """
        colors = [(0, 0, 0), # Color rectangle lines
                  (0, 0, 255),
                  (0, 255, 0),
                  (255, 0, 0),
                  (0, 255, 255),
                  (255, 255, 0)
                ]
        line_thickness = 3 # pts

        img = cv2.imread(self.image)
        
        if isinstance(self.ocr_result, type(None)):
            print("Warning: You must call read_image prior to calling the get_text method!")
        else:
            for index, row in self.ocr_result.iterrows():
                if row['conf'] > 0 and row['width'] * row['height'] > 10: # Check confidence value and that the box has area larger than 10 pixels^2
                    top_coord = (row['left'], row['top']) # left, top
                    bottom_coord = (row['left'] + row['width'], row['top'] + row['height']) # left + width, top + height
                    #print(str(row['block_num']))
                    cv2.rectangle(img, top_coord, bottom_coord, colors[row['block_num']], line_thickness)
        
        cv2.namedWindow("Boxes")
        cv2.imshow("Boxes", img)
        cv2.waitKey()
