import os
import argparse
from fpdf import FPDF
from PIL import Image
from tqdm import tqdm
import PyPDF2  # Make sure this line is included
import io


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


def png_to_pdf(input_folder='.', pdf_filename='output.pdf', verso_image=None):
    pdf = PDF()
    if verso_image == None:
        png_files = [f for f in os.listdir(input_folder) if f.endswith(
            '.png')]
    else:
        png_files = [f for f in os.listdir(input_folder) if f.endswith(
            '.png') and f != os.path.basename(verso_image)]

    if not png_files:
        print("No PNG files found in the specified directory.")
        return

    for png_file in tqdm(png_files, desc="Processing images"):
        pdf.add_page_with_image(os.path.join(input_folder, png_file))
        if verso_image:
            pdf.add_page_with_image(verso_image)

    pdf.output(pdf_filename)
    print(f"PDF created successfully: {pdf_filename}")


def merge_pdfs_and_images(input_folder='.', output_filename='merged.pdf', verso_image=None):
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]
    if verso_image:
        png_files = [f for f in os.listdir(input_folder) if f.endswith(
            '.png') and f != os.path.basename(verso_image)]
    else:
        png_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    if not pdf_files and not png_files:
        print("No PDF or PNG files found in the specified directory.")
        return

    merger = PyPDF2.PdfMerger()

    if png_files:
        pdf = PDF()
        for png_file in tqdm(png_files, desc="Processing images"):
            print(len(png_files))
            pdf.add_page_with_image(os.path.join(input_folder, png_file))
            print("add")
            if verso_image:
                pdf.add_page_with_image(verso_image)

        pdf_bytes = pdf.output()
        pdf_bytes = bytes(pdf_bytes)
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        merger.append(pdf_reader)

    if pdf_files:
        for pdf_file in tqdm(pdf_files, desc="Merging PDFs"):
            merger.append(os.path.join(input_folder, pdf_file))

    merger.write(output_filename)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a PDF from PNG images and merge with existing PDFs.')
    parser.add_argument('-i', '--input', type=str, default='.',
                        help='Path of the input folder containing pictures or PDFs (default: current folder)')
    parser.add_argument('-o', '--output', type=str, default='output.pdf',
                        help='Path of the output generated PDF (default: ./output.pdf)')
    parser.add_argument('-v', '--verso', type=str,
                        help='Path of an image to add after each PNG (verso)')
    parser.add_argument('-t', '--test', action='store_true',
                        help='Run a test to create a PDF from images in the test folder')

    args = parser.parse_args()

    if args.test:
        test_images_to_pdf()
    else:
        merge_pdfs_and_images(args.input, args.output, args.verso)
