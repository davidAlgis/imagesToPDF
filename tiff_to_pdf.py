from PIL import Image
from fpdf import FPDF


class PDF(FPDF):

    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation, unit, format)
        self.set_auto_page_break(0)

    def add_page_with_image(self, image_path, dpi):
        img = Image.open(image_path)
        img_width, img_height = img.size
        # Convert pixel dimensions to mm
        page_width = img_width * 25.4 / dpi
        page_height = img_height * 25.4 / dpi
        self.add_page(format=(page_width, page_height))
        self.image(image_path, 0, 0, page_width, page_height)


def tiff_to_pdf(tif_file, pdf_file, dpi=300, page_format='A4'):
    """
    Convert a TIFF image to a PDF using FPDF.
    """
    pdf = PDF(format=page_format)
    pdf.add_page_with_image(tif_file, dpi)
    pdf.output(pdf_file)
