import os
from psd_tools import PSDImage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def psd_to_pdf(psd_file, pdf_filename, dpi=300):
    """
    Convert a PSD file directly to a PDF, preserving the CMYK format.
    """
    # Open the PSD file
    psd = PSDImage.open(psd_file)

    # Extract dimensions in points (1 point = 1/72 inch)
    img_width, img_height = psd.size
    page_width = img_width * 72 / dpi
    page_height = img_height * 72 / dpi

    # Create the PDF canvas
    c = canvas.Canvas(pdf_filename, pagesize=(page_width, page_height))

    # Save the PSD composite as a temporary CMYK-compatible TIFF
    temp_image_path = "temp_image.tiff"
    psd.composite().save(temp_image_path, "TIFF")

    # Draw the TIFF image directly into the PDF
    c.drawImage(temp_image_path, 0, 0, width=page_width, height=page_height)

    # Finish up the PDF
    c.showPage()
    c.save()

    # Clean up temporary files
    os.remove(temp_image_path)
