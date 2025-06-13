"""
Image Recognition Module

This module provides functionality for recognizing objects in images using
a pre-trained TensorFlow model.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image


class ImageRecognizer:
    """Class for image recognition using pre-trained models."""
    
    def __init__(self, model_name='mobilenet_v2'):
        """
        Initialize the image recognizer with a specified model.
        
        Args:
            model_name (str): Name of the model to use. Default is 'mobilenet_v2'.
        """
        self.model_name = model_name
        self.model = self._load_model()
        
    def _load_model(self):
        """
        Load the pre-trained model.
        
        Returns:
            The loaded model.
        """
        if self.model_name == 'mobilenet_v2':
            return MobileNetV2(weights='imagenet')
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")
    
    def preprocess_image(self, img_path):
        """
        Preprocess an image for the model.
        
        Args:
            img_path (str): Path to the image file.
            
        Returns:
            numpy.ndarray: Preprocessed image.
        """
        try:
            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            return preprocess_input(img_array)
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")
    
    def recognize(self, img_path, top_n=5):
        """
        Recognize objects in an image.
        
        Args:
            img_path (str): Path to the image file.
            top_n (int): Number of top predictions to return.
            
        Returns:
            list: List of tuples (class_name, class_description, score).
        """
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image file not found: {img_path}")
            
        processed_img = self.preprocess_image(img_path)
        predictions = self.model.predict(processed_img)
        results = decode_predictions(predictions, top=top_n)[0]
        
        # Convert to more readable format
        formatted_results = [(label, description, float(score)) 
                            for _, label, description, score in 
                            [(i,) + result for i, result in enumerate(results)]]
        
        return formatted_results
    
    def display_results(self, results):
        """
        Display recognition results in a readable format.
        
        Args:
            results (list): List of recognition results.
        """
        print("\n===== Recognition Results =====")
        for i, (_, description, score) in enumerate(results, 1):
            print(f"{i}. {description} ({score:.2%} confidence)")
        print("=============================")


def recognize_image(image_path, top_n=5):
    """
    Convenience function to recognize objects in an image.
    
    Args:
        image_path (str): Path to the image file.
        top_n (int): Number of top predictions to return.
        
    Returns:
        list: List of recognition results.
    """
    recognizer = ImageRecognizer()
    results = recognizer.recognize(image_path, top_n)
    recognizer.display_results(results)
    return results