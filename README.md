# ImagesToPDF

This Python script automatically generates a PDF file from PNG and PSD images in a specified directory. It includes an option to add a specific image (verso) after each PNG image, split images into two pages, and merge all resulting PDFs into a single PDF.

## Installation

Before running the script, you need to install the required Python libraries. You can install them using the provided requirements.txt file.

```
pip install -r requirements.txt
```

## Usage

Ensure you have Python 3.6 or newer installed on your system. Clone this repository or download the script and requirements.txt file. Install the required libraries as mentioned above. To use the script, run it from the command line with the desired options:

```
python main.py [options]
```

## Options

- `-i`, `--input <directory>`: Specify the directory where PNG and PSD files are located for processing. If not specified, the script uses its current directory.

- `-o`, `--output <file>`: Specify the path of the output PDF file. If not specified, the script saves the PDF as `output.pdf` in the current directory.

- `-v`, `--verso <file>`: Specify the path of an image to add after each PNG or PSD image. The verso image will not be included as a standalone page if it is in the input folder.

- `-s`, `--split <boolean>`: Split each page in the PDF into two along the width (default is False).

- `-d`, `--dpi <integer>`: Specify the DPI (dots per inch) for the PDF generation. Higher values increase the resolution but also the file size (default is 300 DPI).

- `-t`, `--test`: Run a test to create a PDF from images in the test folder.

- `-h`, `--help`: Display help information showing all command-line options.

## Example

To generate a PDF from PNG and PSD images in the `my_images` folder and save it as `my_document.pdf`, use:

```
python main.py -i my_images -o my_document.pdf
```

To include a verso image named `verso.png` in the `my_images` folder:

```
python main.py -i "my_images" -o "my_document.pdf" -v "my_images/verso.png"
```

To split each PNG image into two pages and save the resulting PDF:

```
python main.py -i my_images -o my_document.pdf -s true
```

To specify the DPI as 400 for high-resolution PDFs:

```
python main.py -i my_images -o my_document.pdf -d 400
```

## Notes

- Supported input formats: PNG and PSD.
- The script automatically converts PSD files to TIFF while preserving the CMYK color profile and then to PDF.
- Existing PDFs in the input folder are merged into the output PDF without modification.
