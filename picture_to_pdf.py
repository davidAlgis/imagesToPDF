import os
from fpdf import FPDF
from PIL import Image


class PDF(FPDF):

    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation, unit, format)
        self.set_auto_page_break(0)

    def add_page_with_image(self, image_path):
        try:
            img = Image.open(image_path)
            img_width, img_height = img.size
            # Convert pixel dimensions to mm (assuming 96 DPI)
            page_width = img_width * 25.4 / 96
            page_height = img_height * 25.4 / 96
            self.add_page(format=(page_width, page_height))
            self.image(image_path, 0, 0, page_width, page_height)
        except Exception as e:
            print(f"Error adding image {image_path}: {e}")


def picture_to_pdf(image_file, pdf_filename, verso_image=None, split=False):
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

    # Process the main image
    if split:
        left_img_path, right_img_path = split_image(image_file)
        pdf.add_page_with_image(left_img_path)
        pdf.add_page_with_image(right_img_path)
        os.remove(left_img_path)
        os.remove(right_img_path)
    else:
        pdf.add_page_with_image(image_file)

    # Add the verso image, if provided
    if verso_image:
        pdf.add_page_with_image(verso_image)

    # Save the generated PDF
    pdf.output(pdf_filename)
