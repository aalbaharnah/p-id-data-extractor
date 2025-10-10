# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
import os
import unittest
from unittest.mock import MagicMock, patch
import sys
import io
from PIL import Image
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
from app.services.text_detection.utils.ocr_client import OcrClient


class TestReadText(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        # Create a simple test image
        self.test_image = Image.new('RGB', (100, 50), color='white')
        img_bytes = io.BytesIO()
        self.test_image.save(img_bytes, format='PNG')
        self.test_image_bytes = img_bytes.getvalue()

    @patch('app.services.text_detection.utils.ocr_client.pytesseract.image_to_data')
    def test_happy_path(self, mock_tesseract):
        # arrange
        ocr_client = OcrClient()

        # Mock Tesseract response
        mock_tesseract.return_value = {
            'text': ['', 'test', 'text', '', 'test_text_2', ''],
            'line_num': [1, 1, 1, 2, 2, 3],
            'left': [0, 10, 50, 0, 90, 0],
            'top': [0, 5, 5, 20, 25, 40],
            'width': [0, 30, 30, 0, 60, 0],
            'height': [0, 10, 10, 0, 10, 0]
        }

        # act
        result = ocr_client.read_text(self.test_image_bytes)

        # assert
        actual_results = list(result)
        expected_results = [
            ("test text", [[10, 5], [80, 5], [80, 15], [10, 15]]),
            ("test_text_2", [[90, 25], [150, 25], [150, 35], [90, 35]])
        ]
        self.assertEqual(actual_results, expected_results)
        mock_tesseract.assert_called_once()

    @patch('app.services.text_detection.utils.ocr_client.pytesseract.image_to_data')
    def test_when_tesseract_raises_exception_then_raises_exception(self, mock_tesseract):
        # arrange
        ocr_client = OcrClient()

        mock_tesseract.side_effect = Exception("Tesseract error")

        # act
        with self.assertRaises(Exception) as context:
            list(ocr_client.read_text(self.test_image_bytes))

        # assert
        self.assertIn("OCR processing failed", str(context.exception))
        mock_tesseract.assert_called_once()

    @patch('app.services.text_detection.utils.ocr_client.pytesseract.image_to_data')
    def test_when_no_text_detected_then_returns_empty_generator(self, mock_tesseract):
        # arrange
        ocr_client = OcrClient()

        # Mock Tesseract response with no valid text
        mock_tesseract.return_value = {
            'text': ['', '', ''],
            'line_num': [1, 2, 3],
            'left': [0, 0, 0],
            'top': [0, 0, 0],
            'width': [0, 0, 0],
            'height': [0, 0, 0]
        }

        # act
        result = ocr_client.read_text(self.test_image_bytes)

        # assert
        actual_results = list(result)
        self.assertEqual(actual_results, [])
        mock_tesseract.assert_called_once()

