# 画像認識アプリ (Image Recognition Application)

This is a simple image recognition application that can identify objects in images using pre-trained deep learning models.

## Features

- Recognize objects in images using TensorFlow's pre-trained MobileNetV2 model
- Simple and intuitive graphical user interface
- Command-line interface for batch processing
- Displays top predictions with confidence scores

## Requirements

- Python 3.6 or higher
- TensorFlow 2.5.0 or higher
- NumPy
- Pillow (PIL)
- Matplotlib

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/image-recognition-app.git
   cd image-recognition-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Graphical User Interface

To start the GUI application:

```
python main.py
```

1. Click the "参照..." button to select an image file
2. Click the "認識開始" button to start the recognition process
3. View the results in the results area

### Command Line Interface

To use the command-line interface:

```
python cli.py path/to/your/image.jpg
```

Optional arguments:
- `-n, --top-n`: Number of top predictions to display (default: 5)

Example:
```
python cli.py images/cat.jpg --top-n 3
```

## Testing

To run the tests:

```
python run_tests.py
```

## Project Structure

```
.
├── image_recognition.py  # Core image recognition functionality
├── main.py              # GUI application
├── cli.py               # Command-line interface
├── requirements.txt     # Project dependencies
├── run_tests.py         # Test runner
└── test/                # Test directory
    ├── __init__.py
    ├── test_image_recognition.py
    └── test_data/       # Test data directory
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- TensorFlow team for the pre-trained models
- The Python community for the excellent libraries