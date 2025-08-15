#!/usr/bin/env python3
"""
Demo script for Photo Organizer
This script creates some sample test cases and demonstrates the classification system
"""

import os
import cv2
import numpy as np
from pathlib import Path
from photo_classifier import PhotoClassifier

def create_sample_images():
    """Create sample images for testing different categories"""
    demo_folder = Path("demo_photos")
    demo_folder.mkdir(exist_ok=True)
    
    print("Creating sample demo images...")
    
    # 1. Create a document-like image (white background with black rectangles)
    doc_img = np.ones((800, 600, 3), dtype=np.uint8) * 255  # White background
    cv2.rectangle(doc_img, (50, 100), (550, 150), (0, 0, 0), 2)  # Title box
    cv2.rectangle(doc_img, (50, 200), (550, 250), (0, 0, 0), 2)  # Text box
    cv2.rectangle(doc_img, (50, 300), (550, 350), (0, 0, 0), 2)  # Text box
    cv2.rectangle(doc_img, (50, 400), (550, 450), (0, 0, 0), 2)  # Text box
    
    # Add some text-like patterns
    for i in range(5, 15):
        y = 120 + i * 20
        cv2.line(doc_img, (70, y), (530, y), (0, 0, 0), 1)
    
    cv2.imwrite(str(demo_folder / "sample_document.jpg"), doc_img)
    
    # 2. Create a nature-like image (green and blue)
    nature_img = np.zeros((600, 800, 3), dtype=np.uint8)
    # Sky (blue)
    nature_img[:200, :] = [200, 150, 100]  # Sky blue in BGR
    # Grass (green) 
    nature_img[200:400, :] = [100, 180, 50]  # Green in BGR
    # Trees (darker green)
    nature_img[400:, :] = [80, 120, 40]  # Darker green in BGR
    
    cv2.imwrite(str(demo_folder / "sample_nature.jpg"), nature_img)
    
    # 3. Create a colorful abstract image (will likely be classified as unknown)
    abstract_img = np.random.randint(0, 255, (600, 600, 3), dtype=np.uint8)
    cv2.imwrite(str(demo_folder / "sample_abstract.jpg"), abstract_img)
    
    # 4. Create a simple geometric image
    geometric_img = np.ones((500, 500, 3), dtype=np.uint8) * 128
    cv2.circle(geometric_img, (250, 250), 100, (255, 0, 0), -1)  # Blue circle
    cv2.rectangle(geometric_img, (150, 150), (350, 350), (0, 255, 0), 3)  # Green rectangle
    cv2.imwrite(str(demo_folder / "sample_geometric.jpg"), geometric_img)
    
    print(f"✅ Created 4 sample images in {demo_folder}/")
    return demo_folder

def run_demo():
    """Run the photo organizer demo"""
    print("🤖 Photo Organizer Demo")
    print("=" * 50)
    
    # Create sample images
    demo_folder = create_sample_images()
    
    # Run classification
    print(f"\n📂 Processing images from: {demo_folder}")
    classifier = PhotoClassifier(
        source_folder=str(demo_folder),
        output_folder="demo_organized"
    )
    
    classifier.process_images()
    
    print("\n✅ Demo completed!")
    print("\nCheck the 'demo_organized' folder to see how your photos were classified.")
    print("Note: This demo uses synthetic images, so results may vary with real photos.")
    
    # Clean up demo folder
    response = input("\nDo you want to keep the demo files? (y/n): ").lower().strip()
    if response != 'y':
        import shutil
        if demo_folder.exists():
            shutil.rmtree(demo_folder)
            print("Demo files cleaned up.")

if __name__ == "__main__":
    run_demo()
