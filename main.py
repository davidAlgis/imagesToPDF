import os
import argparse
from fpdf import FPDF
from PIL import Image
from tqdm import tqdm
import PyPDF2
import io
from psd_tools import PSDImage


class PDF(FPDF):
    def add_page_with_image(self, image_path):
        self.add_page()
        img = Image.open(image_path)
        img_width, img_height = img.size
        page_width, page_height = self.w, self.h
        # Scale image to fit page
        if img_width / img_height > page_width / page_height:
            new_width = page_width
            new_height = (page_width / img_width) * img_height
        else:
            new_height = page_height
            new_width = (page_height / img_height) * img_width
        self.image(image_path, x=0, y=0, w=new_width, h=new_height)


def convert_psd_to_png(input_folder='.'):
    png_files = []
    for psd_file in tqdm([f for f in os.listdir(input_folder) if f.endswith('.psd')], desc="Converting PSD to PNG"):
        psd_image = PSDImage.open(os.path.join(input_folder, psd_file))
        png_file = os.path.join(input_folder, psd_file.replace('.psd', '.png'))
        psd_image.composite().save(png_file)
        png_files.append(png_file)
    return png_files


def split_image(image_path):
    img = Image.open(image_path)
    img_width, img_height = img.size
    left_img = img.crop((0, 0, img_width // 2, img_height))
    right_img = img.crop((img_width // 2, 0, img_width, img_height))
    left_img_path = image_path.replace('.png', '_left.png')
    right_img_path = image_path.replace('.png', '_right.png')
    left_img.save(left_img_path)
    right_img.save(right_img_path)
    return left_img_path, right_img_path


def png_to_pdf(input_folder='.', pdf_filename='output.pdf', verso_image=None, split=False):
    pdf = PDF()
    png_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

    if not png_files:
        print("No PNG files found in the specified directory.")
        return

    for png_file in tqdm(png_files, desc="Processing images"):
        if split:
            left_img_path, right_img_path = split_image(
                os.path.join(input_folder, png_file))
            pdf.add_page_with_image(left_img_path)
            pdf.add_page_with_image(right_img_path)
            os.remove(left_img_path)
            os.remove(right_img_path)
        else:
            pdf.add_page_with_image(os.path.join(input_folder, png_file))

        if verso_image:
            pdf.add_page_with_image(verso_image)

    pdf.output(pdf_filename)
    print(f"PDF created successfully: {pdf_filename}")


def merge_pdfs_and_images(input_folder='.', output_filename='merged.pdf', verso_image=None, split=False):
    # Convert PSD files to PNG files first
    psd_converted_files = convert_psd_to_png(input_folder)

    # Add existing PNG files
    all_png_files = [os.path.join(input_folder, f) for f in os.listdir(
        input_folder) if f.endswith('.png')]
    png_files = list(set(all_png_files) - set(psd_converted_files))

    pdf_files = [os.path.join(input_folder, f)
                 for f in os.listdir(input_folder) if f.endswith('.pdf')]

    if not pdf_files and not png_files and not psd_converted_files:
        print("No PDF or image files found in the specified directory.")
        return

    merger = PyPDF2.PdfMerger()

    if psd_converted_files or png_files:
        pdf = PDF()
        for png_file in tqdm(psd_converted_files + png_files, desc="Processing images"):
            if split:
                left_img_path, right_img_path = split_image(png_file)
                pdf.add_page_with_image(left_img_path)
                pdf.add_page_with_image(right_img_path)
                os.remove(left_img_path)
                os.remove(right_img_path)
            else:
                pdf.add_page_with_image(png_file)

            if verso_image:
                pdf.add_page_with_image(verso_image)

        pdf_bytes = pdf.output()
        pdf_bytes = bytes(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        merger.append(pdf_reader)

    if pdf_files:
        for pdf_file in tqdm(pdf_files, desc="Merging PDFs"):
            merger.append(pdf_file)

    with open(output_filename, 'wb') as fout:
        merger.write(fout)

    merger.close()
    print(f"PDFs and images merged successfully: {output_filename}")


def test_images_to_pdf():
    test_folder = 'test'
    test_output = 'test_output.pdf'
    verso_image = os.path.join(test_folder, 'verso.png')
    try:
        png_to_pdf(test_folder, test_output, verso_image)
        if os.path.exists(test_output):
            os.remove(test_output)
            print(f"PDF removed after test: {test_output}")
            print("ImagesToPDF test has succeeded!")
        else:
            print("ImagesToPDF test has failed!")
    except Exception as e:
        print(f"ImagesToPDF test has failed! Error: {e}")


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

    if args.test:
        test_images_to_pdf()
    else:
        merge_pdfs_and_images(args.input, args.output, args.verso, args.split)
