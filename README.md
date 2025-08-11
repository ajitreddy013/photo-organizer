# Photo Organizer

An intelligent photo classification system that automatically sorts your photos into different categories:

- **Documents**: Screenshots, scanned documents, text-heavy images
- **Selfies**: Self-portraits with a single person's face prominently displayed
- **People**: Photos containing people (groups, portraits, etc.)
- **Nature**: Landscape photos, sky, greenery, outdoor scenes
- **Unknown**: Photos that don't fit into other categories

## Features

- **Computer Vision Based**: Uses OpenCV for face detection and image analysis
- **Automatic Classification**: No manual tagging required
- **Batch Processing**: Processes entire folders at once
- **Safe Operations**: Copies files (doesn't move them) to preserve originals
- **Conflict Resolution**: Handles duplicate filenames automatically

## Installation

### Option 1: Quick Setup
```bash
# Install required packages
pip install opencv-python numpy Pillow

# Run directly
python photo_classifier.py /path/to/your/photos
```

### Option 2: Full Installation
```bash
# Clone or download this project
cd photo-organizer

# Install in development mode
pip install -e .

# Or install requirements manually
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
# Organize photos from a source folder
python photo_classifier.py /path/to/your/photos

# Specify custom output folder
python photo_classifier.py /path/to/your/photos -o /path/to/organized_photos
```

### Advanced Usage
```python
from photo_classifier import PhotoClassifier

# Create classifier instance
classifier = PhotoClassifier(
    source_folder="/path/to/your/photos",
    output_folder="/path/to/organized_photos"
)

# Process all images
classifier.process_images()
```

## How It Works

The classifier uses several computer vision techniques:

### Document Detection
- Analyzes image for rectangular patterns
- Detects horizontal lines (typical of text)
- Checks aspect ratios common in documents

### Face Detection
- Uses Haar cascade classifiers for face detection
- Distinguishes between selfies and group photos based on:
  - Number of faces
  - Face size relative to image
  - Face position in frame

### Nature Detection
- Analyzes color distribution in HSV color space
- Identifies predominant green (vegetation) and blue (sky) regions
- Classifies based on color percentages

## Supported Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WebP (.webp)

## Output Structure

After processing, your photos will be organized like this:
```
organized_photos/
├── documents/
├── selfies/
├── people/
├── nature/
└── unknown/
```

## Requirements

- Python 3.7+
- OpenCV (opencv-python)
- NumPy
- Pillow

## Limitations

- Classification accuracy depends on image quality and content
- May misclassify ambiguous images
- Requires good lighting for face detection
- Document detection works best with clear, high-contrast text

## Tips for Better Results

1. **Good Quality Images**: Higher resolution images generally classify better
2. **Clear Lighting**: Well-lit photos improve face detection accuracy
3. **Review Results**: Check the "unknown" folder for misclassified images
4. **Manual Adjustment**: Feel free to move images between folders after processing

## Troubleshooting

### Common Issues

1. **No faces detected**: Check image quality and lighting
2. **Documents misclassified**: Ensure documents have clear text and good contrast
3. **Nature photos in wrong category**: Adjust color thresholds if needed

### Error Messages

- "Could not load image": File might be corrupted or unsupported format
- "Source folder does not exist": Check the path to your photos folder

## Example

```bash
# Process photos from Downloads folder
python photo_classifier.py ~/Downloads/Photos

# Output will be created in organized_photos/ folder
```

Sample output:
```
==================================================
CLASSIFICATION SUMMARY
==================================================
Documents: 15 images
Selfies: 8 images
People: 23 images
Nature: 31 images
Unknown: 12 images
Total processed: 89 images

Output folder: /Users/ajitreddy/organized_photos
```
