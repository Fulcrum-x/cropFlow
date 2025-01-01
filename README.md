# CropFlow

CropFlow is a powerful, user-friendly desktop application for batch converting PNG images to high-quality JPG format with advanced cropping and HDR tone mapping capabilities.

![CropFlow Interface](placeholder-for-screenshot.png)

## Features

- **Batch PNG to JPG Conversion**: Convert multiple PNG images at once while maintaining high quality
- **Smart Aspect Ratio Cropping**: Multiple preset options including:
  - 16:9 (Widescreen)
  - 1.85:1 (Digital Cinema)
  - 2.39:1 (Anamorphic)
  - 4:3 (Standard)
  - Original aspect ratio
- **Automatic Letterbox Detection**: Automatically detects and removes black bars from images
- **HDR Tone Mapping**: Three professional-grade tone mapping algorithms:
  - Reinhard (Default): Excellent for general-purpose HDR conversion
  - Drago: Enhanced detail preservation in dark areas
  - Mantiuk: Optimized for high-contrast scenes
- **Customizable Settings**:
  - Adjustable JPEG quality (1-100)
  - Tone mapping intensity control
  - Transparent PNG handling with white background conversion

## Installation

1. Ensure you have Python 3.6 or higher installed
2. Install required dependencies:
```bash
pip install Pillow numpy opencv-python
```

3. Download or clone the repository:
```bash
git clone https://github.com/yourusername/cropflow.git
cd cropflow
```

4. Run the application:
```bash
python cropflow.py
```

## Usage

1. Launch CropFlow
2. Click "Browse" to select a folder containing PNG images
3. Choose desired aspect ratio from the dropdown menu
4. Select HDR tone mapping method if needed
5. Adjust tone mapping intensity (gamma) if desired
6. Set JPEG quality (default: 95)
7. Click "Convert Images" to begin the batch process

The application will process all PNG images in the selected folder, maintaining the original file names but changing the extension to .jpg.

## Requirements

- Python 3.6+
- Pillow (PIL)
- NumPy
- OpenCV Python

## Known Limitations

- Currently processes PNG files only
- Source images must be in the same folder
- Processes all PNG files in selected folder

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenCV for HDR tone mapping algorithms
- Pillow (PIL) for image processing
- NumPy for numerical operations

## Support

If you encounter any issues or have questions, please:
1. Check the [Issues](https://github.com/yourusername/cropflow/issues) page
2. Open a new issue if your problem isn't already listed

## Roadmap

Future features under consideration:
- Support for additional image formats (JPEG, WEBP, etc.)
- Custom aspect ratio input
- Batch resize options
- Output folder selection
- Preview window for tone mapping results
