#!/usr/bin/env python3
"""
Example usage of the Photo Organizer

This script demonstrates different ways to use the photo classifier
"""

from photo_classifier import PhotoClassifier
import os
from pathlib import Path

def example_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Example ===")
    
    # Replace with your actual photo folder path
    source_folder = input("Enter the path to your photos folder: ").strip()
    
    if not os.path.exists(source_folder):
        print(f"Error: Folder '{source_folder}' does not exist!")
        return
    
    # Create classifier
    classifier = PhotoClassifier(
        source_folder=source_folder,
        output_folder="organized_photos"
    )
    
    # Process images
    classifier.process_images()
    print("\nDone! Check the 'organized_photos' folder for your sorted images.")

def example_custom_output():
    """Example with custom output folder"""
    print("\n=== Custom Output Folder Example ===")
    
    source_folder = input("Enter the path to your photos folder: ").strip()
    output_folder = input("Enter the output folder name (or press Enter for default): ").strip()
    
    if not output_folder:
        output_folder = "my_organized_photos"
    
    if not os.path.exists(source_folder):
        print(f"Error: Folder '{source_folder}' does not exist!")
        return
    
    classifier = PhotoClassifier(
        source_folder=source_folder,
        output_folder=output_folder
    )
    
    classifier.process_images()
    print(f"\nDone! Check the '{output_folder}' folder for your sorted images.")

def example_batch_multiple_folders():
    """Example processing multiple folders"""
    print("\n=== Multiple Folders Example ===")
    
    # List of folders to process (you can modify this)
    folders_to_process = []
    
    while True:
        folder = input("Enter a photo folder path (or 'done' to finish): ").strip()
        if folder.lower() == 'done':
            break
        if os.path.exists(folder):
            folders_to_process.append(folder)
        else:
            print(f"Warning: '{folder}' does not exist, skipping...")
    
    if not folders_to_process:
        print("No valid folders to process.")
        return
    
    # Process each folder
    for i, folder in enumerate(folders_to_process):
        print(f"\nProcessing folder {i+1}/{len(folders_to_process)}: {folder}")
        
        output_folder = f"organized_photos_batch_{i+1}"
        classifier = PhotoClassifier(
            source_folder=folder,
            output_folder=output_folder
        )
        
        classifier.process_images()
        print(f"Folder {i+1} complete! Output: {output_folder}")
    
    print(f"\nAll {len(folders_to_process)} folders processed!")

def show_supported_formats():
    """Show supported image formats"""
    print("\n=== Supported Image Formats ===")
    formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp']
    for fmt in formats:
        print(f"  • {fmt.upper()}")

def main():
    """Main example runner"""
    print("Photo Organizer - Example Usage")
    print("===============================")
    
    while True:
        print("\nChoose an example to run:")
        print("1. Basic usage")
        print("2. Custom output folder")
        print("3. Process multiple folders")
        print("4. Show supported formats")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            example_basic_usage()
        elif choice == '2':
            example_custom_output()
        elif choice == '3':
            example_batch_multiple_folders()
        elif choice == '4':
            show_supported_formats()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
