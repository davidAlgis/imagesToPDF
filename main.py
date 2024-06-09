import os
from fpdf import FPDF
from PIL import Image


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


def png_to_pdf(pdf_filename='output.pdf'):
    pdf = PDF()
    png_files = [f for f in os.listdir('.') if f.endswith('.png')]

    if not png_files:
        print("No PNG files found in the current directory.")
        return

    for png_file in png_files:
        pdf.add_page_with_image(png_file)

    pdf.output(pdf_filename)
    print(f"PDF created successfully: {pdf_filename}")


if __name__ == '__main__':
    png_to_pdf()
