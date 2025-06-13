"""
Unit tests for the image recognition module.
"""

import os
import unittest
import tempfile
from unittest.mock import patch, MagicMock
import numpy as np

# Add parent directory to path to import the module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from image_recognition import ImageRecognizer


class TestImageRecognizer(unittest.TestCase):
    """Test cases for the ImageRecognizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # Create a small test image if it doesn't exist
        self.test_image_path = os.path.join(self.test_data_dir, 'test_image.jpg')
        if not os.path.exists(self.test_image_path):
            # Create a simple 10x10 black image
            try:
                from PIL import Image
                img = Image.new('RGB', (10, 10), color='black')
                img.save(self.test_image_path)
            except ImportError:
                # If PIL is not available, create an empty file
                with open(self.test_image_path, 'w') as f:
                    f.write('')
    
    def test_init(self):
        """Test initializing the ImageRecognizer."""
        recognizer = ImageRecognizer()
        self.assertEqual(recognizer.model_name, 'mobilenet_v2')
        self.assertIsNotNone(recognizer.model)
    
    def test_init_invalid_model(self):
        """Test initializing with an invalid model name."""
        with self.assertRaises(ValueError):
            ImageRecognizer(model_name='invalid_model')
    
    @patch('image_recognition.image.load_img')
    @patch('image_recognition.image.img_to_array')
    @patch('image_recognition.preprocess_input')
    def test_preprocess_image(self, mock_preprocess, mock_img_to_array, mock_load_img):
        """Test preprocessing an image."""
        # Mock the image processing functions
        mock_load_img.return_value = MagicMock()
        mock_img_to_array.return_value = np.zeros((224, 224, 3))
        mock_preprocess.return_value = np.zeros((1, 224, 224, 3))
        
        recognizer = ImageRecognizer()
        result = recognizer.preprocess_image(self.test_image_path)
        
        # Check that the functions were called correctly
        mock_load_img.assert_called_once_with(self.test_image_path, target_size=(224, 224))
        mock_img_to_array.assert_called_once()
        mock_preprocess.assert_called_once()
        
        # Check the result shape
        self.assertEqual(result.shape, (1, 224, 224, 3))
    
    def test_preprocess_image_invalid_path(self):
        """Test preprocessing with an invalid image path."""
        recognizer = ImageRecognizer()
        with self.assertRaises(ValueError):
            recognizer.preprocess_image('/invalid/path/to/image.jpg')
    
    @patch('image_recognition.ImageRecognizer.preprocess_image')
    def test_recognize(self, mock_preprocess):
        """Test recognizing objects in an image."""
        # Mock the preprocessing and model prediction
        mock_preprocess.return_value = np.zeros((1, 224, 224, 3))
        
        recognizer = ImageRecognizer()
        recognizer.model = MagicMock()
        recognizer.model.predict.return_value = np.zeros((1, 1000))
        
        # Mock decode_predictions to return sample results
        sample_results = [
            ('n01440764', 'tench', 0.9),
            ('n01443537', 'goldfish', 0.05),
            ('n01484850', 'great_white_shark', 0.02),
            ('n01491361', 'tiger_shark', 0.015),
            ('n01494475', 'hammerhead', 0.005)
        ]
        
        with patch('image_recognition.decode_predictions', return_value=[[sample_results]]):
            results = recognizer.recognize(self.test_image_path)
            
            # Check that we got the expected number of results
            self.assertEqual(len(results), 5)
            
            # Check the format of the results
            for i, (_, description, score) in enumerate(results):
                self.assertEqual(description, sample_results[i][1])
                self.assertEqual(score, sample_results[i][2])
    
    def test_recognize_nonexistent_file(self):
        """Test recognizing with a nonexistent file."""
        recognizer = ImageRecognizer()
        with self.assertRaises(FileNotFoundError):
            recognizer.recognize('/nonexistent/image.jpg')
    
    def test_display_results(self):
        """Test displaying results."""
        recognizer = ImageRecognizer()
        sample_results = [
            (0, 'tench', 0.9),
            (1, 'goldfish', 0.05),
            (2, 'great_white_shark', 0.02)
        ]
        
        # Capture stdout to check the output
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            recognizer.display_results(sample_results)
        
        output = f.getvalue()
        self.assertIn("Recognition Results", output)
        self.assertIn("1. tench (90.00% confidence)", output)
        self.assertIn("2. goldfish (5.00% confidence)", output)
        self.assertIn("3. great_white_shark (2.00% confidence)", output)


if __name__ == '__main__':
    unittest.main()