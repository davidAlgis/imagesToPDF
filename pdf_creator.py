import os
from psd_to_png import convert_psd_to_png
from psd_to_pdf import psd_to_pdf
from png_to_pdf import png_to_pdf
from pdf_merger import merge_pdfs
from tqdm import tqdm
import shutil


def create_pdf(input_folder, output_pdf, verso_image=None, split=False, dpi=96):
    os.makedirs("temp_pdf", exist_ok=True)

    # Handle PSD files directly
    for psd_file in tqdm([f for f in os.listdir(input_folder) if f.endswith('.psd')], desc="Converting PSD to PDF"):
        psd_to_pdf(os.path.join(input_folder, psd_file), os.path.join(
            "temp_pdf", f"{os.path.splitext(psd_file)[0]}.pdf"), dpi)

    # Convert PNG to PDF
    png_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]
    for png_file in tqdm(png_files, desc="Converting PNG to PDF"):
        png_to_pdf(os.path.join(input_folder, png_file), os.path.join(
            "temp_pdf", f"{os.path.splitext(png_file)[0]}.pdf"), verso_image, split, dpi)

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
