# ImagesToPDF

This Python script automatically generates a PDF file from PNG images in a specified directory. It includes an option to add a specific image (verso) after each PNG image and a test function to verify the script's functionality.

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

- `-i`, `--input <directory>`: Specify the directory where PNG files are located for processing. If not specified, the script uses its current directory.

- `-o`, `--output <file>`: Specify the path of the output PDF file. If not specified, the script saves the PDF as output.pdf in the current directory.

- `-v`, `--verso <file>`: Specify the path of an image to add after each PNG image. The verso image will not be included as a standalone page if it is in the input folder.
 
- `-t`, `--test`: Execute a test function to verify the script's functionality. It looks for PNG images in a test folder and an image named "verso.png". If the test succeeds, it prints "ImagesToPDF test has succeeded!" and removes the generated PDF. If the test fails, it prints "ImagesToPDF test has failed!". If the test folder doesn't not exists, the test won't work !

- `-h`, `--help`: Display help information showing all command-line options.

## Example

To generate a PDF from PNG images in the `my_images` folder and save it as my_document.pdf, you would use:

```
python main.py -i my_images -o my_document.pdf
```

To include a verso image named verso.png in the `my_images` folder:

```
python main.py -i "my_images" -o "my_documents.pdf" -v "my_images/verso.png"
```

To run the test function:

```
python main.py --test
```
