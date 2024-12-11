import os
import argparse
from pdf_creator import create_pdf


def str2bool(v):
    """
    Converts a string argument to a boolean value.
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        'Generate a PDF from PNG and PSD images and merge with existing PDFs.')
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        required=True,
        help='Path to an input file or folder containing pictures or PDFs')
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        default='output.pdf',
        help='Path of the output generated PDF (default: ./output.pdf)')
    parser.add_argument(
        '-v',
        '--verso',
        type=str,
        help='Path of an image to add after each PNG or PSD (verso)')
    parser.add_argument(
        '-s',
        '--split',
        type=str2bool,
        default=False,
        help=
        'Split each page in the PDF into two along the width (default is False)'
    )
    parser.add_argument(
        '-t',
        '--test',
        action='store_true',
        help='Run a test to create a PDF from images in the test folder')
    parser.add_argument(
        '-d',
        '--dpi',
        type=int,
        default=300,
        help='DPI to use for PDF generation (default: 300 DPI)')

    args = parser.parse_args()
    input_path = os.path.abspath(args.input)

    # Check if input is a file or folder
    if not os.path.exists(input_path):
        print(f"Input path {input_path} does not exist.")
    elif os.path.isfile(input_path):
        # If input is a file, process it directly
        create_pdf([input_path], args.output, args.verso, args.split, args.dpi)
    elif os.path.isdir(input_path):
        # If input is a directory, pass it to create_pdf
        create_pdf(input_path, args.output, args.verso, args.split, args.dpi)
    else:
        print(f"Invalid input path: {input_path}")
