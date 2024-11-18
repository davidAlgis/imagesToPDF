import os
from psd_to_tiff import psd_to_tiff
from tiff_to_pdf import tiff_to_pdf
from png_to_pdf import png_to_pdf
from pdf_merger import merge_pdfs
from tqdm import tqdm
import shutil


def create_pdf(input_folder,
               output_pdf,
               verso_image=None,
               split=False,
               dpi=96):
    os.makedirs("temp_pdf", exist_ok=True)

    # Handle PSD files directly
    for psd_file in tqdm(
        [f for f in os.listdir(input_folder) if f.endswith('.psd')],
            desc="Converting PSD to TIFF"):
        tif_file = os.path.join("temp_pdf",
                                f"{os.path.splitext(psd_file)[0]}.tiff")
        psd_to_tiff(os.path.join(input_folder, psd_file), tif_file)

        # Convert TIFF to PDF
        pdf_file = tif_file.replace('.tiff', '.pdf')
        tiff_to_pdf(tif_file, pdf_file, dpi)

    # Convert PNG to PDF
    png_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    for png_file in tqdm(png_files, desc="Converting PNG to PDF"):
        png_to_pdf(
            os.path.join(input_folder, png_file),
            os.path.join("temp_pdf", f"{os.path.splitext(png_file)[0]}.pdf"),
            verso_image, split, dpi)

    # Copy existing PDFs to temp_pdf folder
    pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]
    for pdf_file in tqdm(pdf_files, desc="Copying existing PDFs"):
        shutil.copy(os.path.join(input_folder, pdf_file),
                    os.path.join("temp_pdf", pdf_file))

    # Merge PDFs
    merge_pdfs("temp_pdf", output_pdf)

    # Clean up temporary files
    for file in os.listdir("temp_pdf"):
        os.remove(os.path.join("temp_pdf", file))
    os.rmdir("temp_pdf")
