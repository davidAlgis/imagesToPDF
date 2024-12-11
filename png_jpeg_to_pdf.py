from PIL import Image
from fpdf import FPDF
import os


class PDF(FPDF):

    def __init__(self, orientation='P', unit='mm'):
        super().__init__(orientation, unit)
        self.set_auto_page_break(0)

    def add_page_with_image(self, image_path, dpi):
        img = Image.open(image_path)
        img_width, img_height = img.size
        # Convert pixel dimensions to mm
        page_width = img_width * 25.4 / dpi
        page_height = img_height * 25.4 / dpi
        self.add_page(format=(page_width, page_height))
        self.image(image_path, 0, 0, page_width, page_height)


def image_to_pdf(image_file,
                 pdf_filename,
                 verso_image=None,
                 split=False,
                 dpi=300):
    """
    Convert an image file (JPEG or PNG) to a PDF.
    :param image_file: Path to the image file (JPEG or PNG).
    :param pdf_filename: Path to the output PDF file.
    :param verso_image: Path to an optional verso image to add after each page.
    :param split: Whether to split the image into two pages along the width.
    :param dpi: DPI to use for converting image dimensions to PDF dimensions.
    """
    pdf = PDF()

    def split_image(image_path):
        img = Image.open(image_path)
        img_width, img_height = img.size
        left_img = img.crop((0, 0, img_width // 2, img_height))
        right_img = img.crop((img_width // 2, 0, img_width, img_height))
        left_img_path = image_path.replace(
            os.path.splitext(image_path)[1], '_left.png')
        right_img_path = image_path.replace(
            os.path.splitext(image_path)[1], '_right.png')
        left_img.save(left_img_path)
        right_img.save(right_img_path)
        return left_img_path, right_img_path

    if split:
        left_img_path, right_img_path = split_image(image_file)
        pdf.add_page_with_image(left_img_path, dpi)
        pdf.add_page_with_image(right_img_path, dpi)
        os.remove(left_img_path)
        os.remove(right_img_path)
    else:
        pdf.add_page_with_image(image_file, dpi)

    if verso_image:
        pdf.add_page_with_image(verso_image, dpi)

    pdf.output(pdf_filename)


def jpeg_to_pdf(jpeg_file,
                pdf_filename,
                verso_image=None,
                split=False,
                dpi=300):
    """
    Convert a JPEG file directly to a PDF.
    :param jpeg_file: Path to the JPEG file.
    :param pdf_filename: Path to the output PDF file.
    :param verso_image: Optional verso image.
    :param split: Whether to split the image into two pages along the width.
    :param dpi: DPI to use for PDF dimensions.
    """
    image_to_pdf(jpeg_file, pdf_filename, verso_image, split, dpi)


def png_to_pdf(png_file, pdf_filename, verso_image=None, split=False, dpi=300):
    """
    Convert a PNG file directly to a PDF.
    :param png_file: Path to the PNG file.
    :param pdf_filename: Path to the output PDF file.
    :param verso_image: Optional verso image.
    :param split: Whether to split the image into two pages along the width.
    :param dpi: DPI to use for PDF dimensions.
    """
    image_to_pdf(png_file, pdf_filename, verso_image, split, dpi)
