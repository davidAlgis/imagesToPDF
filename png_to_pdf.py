from PIL import Image
from fpdf import FPDF


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


def png_to_pdf(png_file, pdf_filename, verso_image=None, split=False, dpi=300):
    pdf = PDF()

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

    if split:
        left_img_path, right_img_path = split_image(png_file)
        pdf.add_page_with_image(left_img_path, dpi)
        pdf.add_page_with_image(right_img_path, dpi)
        os.remove(left_img_path)
        os.remove(right_img_path)
    else:
        pdf.add_page_with_image(png_file, dpi)

    if verso_image:
        pdf.add_page_with_image(verso_image, dpi)

    pdf.output(pdf_filename)
