# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
import pytesseract
from PIL import Image
import io
import cv2
import numpy as np


class OcrClient(object):
    '''
    Client for reading text from an image using Tesseract OCR.
    '''
    def __init__(self):
        # Configure Tesseract for better OCR results
        self.tesseract_config = '--oem 3 --psm 6'

    def read_text(self, image):
        '''
        Reads text from an image and returns a generator of tuples containing the text and bounding box of each line.
        :param image: Image stream to read in the form of bytes.
        :type image: bytes
        '''
        try:
            # Convert bytes to PIL Image
            pil_image = Image.open(io.BytesIO(image))
            
            # Convert PIL image to numpy array for OpenCV processing
            cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Get detailed data from Tesseract including bounding boxes
            data = pytesseract.image_to_data(cv_image, config=self.tesseract_config, output_type=pytesseract.Output.DICT)
            
            # Group words into lines based on line numbers
            lines = {}
            for i in range(len(data['text'])):
                # Skip empty text
                if data['text'][i].strip() == '':
                    continue
                    
                line_num = data['line_num'][i]
                if line_num not in lines:
                    lines[line_num] = {
                        'words': [],
                        'boxes': []
                    }
                
                lines[line_num]['words'].append(data['text'][i])
                lines[line_num]['boxes'].append({
                    'x': data['left'][i],
                    'y': data['top'][i],
                    'w': data['width'][i],
                    'h': data['height'][i]
                })
            
            # Convert lines to the expected format
            for line_num, line_data in lines.items():
                if not line_data['words']:
                    continue
                    
                # Combine words into line text
                line_text = ' '.join(line_data['words'])
                
                # Calculate bounding box for the entire line
                boxes = line_data['boxes']
                min_x = min(box['x'] for box in boxes)
                min_y = min(box['y'] for box in boxes)
                max_x = max(box['x'] + box['w'] for box in boxes)
                max_y = max(box['y'] + box['h'] for box in boxes)
                
                # Create polygon in the format expected by the rest of the system
                # Format: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                polygon = [
                    [min_x, min_y],  # top-left
                    [max_x, min_y],  # top-right
                    [max_x, max_y],  # bottom-right
                    [min_x, max_y]   # bottom-left
                ]
                
                yield (line_text, polygon)
                
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")


# Initialize OCR client
ocr_client = OcrClient()
