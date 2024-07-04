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
        description='Generate a PDF from PNG and PSD images and merge with existing PDFs.')
    parser.add_argument('-i', '--input', type=str, default='.',
                        help='Path of the input folder containing pictures or PDFs (default: current folder)')
    parser.add_argument('-o', '--output', type=str, default='output.pdf',
                        help='Path of the output generated PDF (default: ./output.pdf)')
    parser.add_argument('-v', '--verso', type=str,
                        help='Path of an image to add after each PNG or PSD (verso)')
    parser.add_argument('-s', '--split', type=str2bool, default=False,
                        help='Split each page in the PDF into two along the width (default is False)')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Run a test to create a PDF from images in the test folder')

    args = parser.parse_args()

    create_pdf(args.input, args.output, args.verso, args.split)
