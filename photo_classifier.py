import os
import shutil
import cv2
import numpy as np
from pathlib import Path
import argparse
from typing import Dict, List, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PhotoClassifier:
    def __init__(self, source_folder: str, output_folder: str):
        self.source_folder = Path(source_folder)
        self.output_folder = Path(output_folder)
        
        # Create output directories
        self.categories = {
            'documents': self.output_folder / 'documents',
            'selfies': self.output_folder / 'selfies',
            'people': self.output_folder / 'people',
            'nature': self.output_folder / 'nature',
            'unknown': self.output_folder / 'unknown'
        }
        
        # Create directories if they don't exist
        for category_path in self.categories.values():
            category_path.mkdir(parents=True, exist_ok=True)
        
        # Load OpenCV face detector
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Supported image extensions
        self.supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
        
    def is_document(self, image: np.ndarray) -> bool:
        """
        Detect if image is a document based on text-like patterns
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to get binary image
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Check for rectangular patterns (typical of documents)
            rectangular_contours = 0
            for contour in contours:
                # Approximate contour to polygon
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Check if contour is rectangular and of reasonable size
                if len(approx) == 4 and cv2.contourArea(contour) > 1000:
                    rectangular_contours += 1
            
            # Check aspect ratio (documents tend to have standard ratios)
            height, width = gray.shape
            aspect_ratio = width / height
            
            # Documents often have more horizontal lines
            edges = cv2.Canny(gray, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
            
            horizontal_lines = 0
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    angle = abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
                    if angle < 10 or angle > 170:  # Nearly horizontal
                        horizontal_lines += 1
            
            # Document criteria: multiple rectangular shapes, reasonable aspect ratio, horizontal lines
            return (rectangular_contours > 2 and 
                    0.7 <= aspect_ratio <= 1.5 and 
                    horizontal_lines > 3)
            
        except Exception as e:
            logger.error(f"Error in document detection: {e}")
            return False
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in the image and return their bounding boxes
        """
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            return faces.tolist() if len(faces) > 0 else []
        except Exception as e:
            logger.error(f"Error in face detection: {e}")
            return []
    
    def is_selfie(self, image: np.ndarray, faces: List[Tuple[int, int, int, int]]) -> bool:
        """
        Determine if image is a selfie based on face size and position
        """
        if len(faces) != 1:  # Selfies typically have one person
            return False
        
        height, width = image.shape[:2]
        x, y, w, h = faces[0]
        
        # Calculate face area relative to image
        face_area = w * h
        image_area = width * height
        face_ratio = face_area / image_area
        
        # Calculate face position (selfies often have face in upper portion)
        face_center_y = y + h // 2
        upper_third = height // 3
        
        # Selfie criteria: large face ratio, face in upper portion
        return (face_ratio > 0.1 and  # Face takes up significant portion
                face_center_y < upper_third * 2 and  # Face in upper 2/3
                w > width * 0.2)  # Face width is significant
    
    def is_nature(self, image: np.ndarray) -> bool:
        """
        Detect nature images based on color distribution and patterns
        """
        try:
            # Convert to HSV for better color analysis
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Define color ranges for green (vegetation) and blue (sky)
            green_lower = np.array([40, 40, 40])
            green_upper = np.array([80, 255, 255])
            blue_lower = np.array([100, 50, 50])
            blue_upper = np.array([130, 255, 255])
            
            # Create masks for green and blue regions
            green_mask = cv2.inRange(hsv, green_lower, green_upper)
            blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
            
            # Calculate percentage of green and blue pixels
            total_pixels = image.shape[0] * image.shape[1]
            green_percentage = np.sum(green_mask > 0) / total_pixels
            blue_percentage = np.sum(blue_mask > 0) / total_pixels
            
            # Nature images typically have significant green or blue content
            return green_percentage > 0.3 or blue_percentage > 0.3 or (green_percentage + blue_percentage) > 0.4
            
        except Exception as e:
            logger.error(f"Error in nature detection: {e}")
            return False
    
    def classify_image(self, image_path: Path) -> str:
        """
        Classify a single image and return the category
        """
        try:
            # Load image
            image = cv2.imread(str(image_path))
            if image is None:
                logger.warning(f"Could not load image: {image_path}")
                return 'unknown'
            
            # Check if it's a document first
            if self.is_document(image):
                return 'documents'
            
            # Detect faces
            faces = self.detect_faces(image)
            
            # Check if it's a selfie
            if self.is_selfie(image, faces):
                return 'selfies'
            
            # Check if it has people (but not selfie)
            if len(faces) > 0:
                return 'people'
            
            # Check if it's nature
            if self.is_nature(image):
                return 'nature'
            
            return 'unknown'
            
        except Exception as e:
            logger.error(f"Error classifying {image_path}: {e}")
            return 'unknown'
    
    def process_images(self):
        """
        Process all images in the source folder
        """
        if not self.source_folder.exists():
            logger.error(f"Source folder does not exist: {self.source_folder}")
            return
        
        # Get all image files
        image_files = []
        for ext in self.supported_extensions:
            image_files.extend(self.source_folder.glob(f"*{ext}"))
            image_files.extend(self.source_folder.glob(f"*{ext.upper()}"))
        
        if not image_files:
            logger.warning("No image files found in source folder")
            return
        
        logger.info(f"Found {len(image_files)} image files to process")
        
        # Process each image
        results = {'documents': 0, 'selfies': 0, 'people': 0, 'nature': 0, 'unknown': 0}
        
        for image_path in image_files:
            logger.info(f"Processing: {image_path.name}")
            
            # Classify image
            category = self.classify_image(image_path)
            
            # Copy to appropriate folder
            destination = self.categories[category] / image_path.name
            
            # Handle filename conflicts
            counter = 1
            while destination.exists():
                name_parts = image_path.stem, counter, image_path.suffix
                destination = self.categories[category] / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                counter += 1
            
            try:
                shutil.copy2(image_path, destination)
                results[category] += 1
                logger.info(f"  -> Classified as: {category}")
            except Exception as e:
                logger.error(f"Error copying {image_path}: {e}")
        
        # Print summary
        print("\n" + "="*50)
        print("CLASSIFICATION SUMMARY")
        print("="*50)
        for category, count in results.items():
            print(f"{category.capitalize()}: {count} images")
        print(f"Total processed: {sum(results.values())} images")
        print(f"\nOutput folder: {self.output_folder}")

def main():
    parser = argparse.ArgumentParser(description="Automatically classify and organize photos")
    parser.add_argument("source_folder", help="Path to folder containing photos to classify")
    parser.add_argument("-o", "--output", help="Output folder for organized photos", 
                       default="organized_photos")
    
    args = parser.parse_args()
    
    # Initialize classifier
    classifier = PhotoClassifier(args.source_folder, args.output)
    
    # Process images
    classifier.process_images()

if __name__ == "__main__":
    main()
