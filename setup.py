from setuptools import setup, find_packages

setup(
    name="photo-organizer",
    version="1.0.0",
    description="Automatically classify and organize photos into categories",
    author="Photo Organizer",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "Pillow>=10.0.0",
    ],
    entry_points={
        'console_scripts': [
            'photo-organizer=photo_classifier:main',
        ],
    },
    python_requires='>=3.7',
)
