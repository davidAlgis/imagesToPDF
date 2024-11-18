import os
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

from psd_to_tiff import psd_to_tiff
from tiff_to_pdf import tiff_to_pdf
from png_to_pdf import png_to_pdf
from pdf_merger import merge_pdfs


def process_psd(psd_file, temp_dir, dpi):
    """Convert PSD to TIFF and then to PDF."""
    tif_file = os.path.join(
        temp_dir, f"{os.path.splitext(os.path.basename(psd_file))[0]}.tiff")
    pdf_file = tif_file.replace('.tiff', '.pdf')
    psd_to_tiff(psd_file, tif_file)
    tiff_to_pdf(tif_file, pdf_file, dpi)
    return pdf_file


def process_png(png_file, temp_dir, verso_image, split, dpi):
    """Convert PNG to PDF."""
    pdf_file = os.path.join(
        temp_dir, f"{os.path.splitext(os.path.basename(png_file))[0]}.pdf")
    png_to_pdf(png_file, pdf_file, verso_image, split, dpi)
    return pdf_file


def copy_pdf(pdf_file, temp_dir):
    """Copy an existing PDF to the temp directory."""
    dest_file = os.path.join(temp_dir, os.path.basename(pdf_file))
    shutil.copy(pdf_file, dest_file)
    return dest_file


def create_pdf(input_folder,
               output_pdf,
               verso_image=None,
               split=False,
               dpi=96):
    temp_dir = os.path.abspath("temp_pdf")
    os.makedirs(temp_dir, exist_ok=True)

    input_folder = os.path.abspath(input_folder)
    psd_files = [
        os.path.join(input_folder, f) for f in os.listdir(input_folder)
        if f.endswith('.psd')
    ]
    png_files = [
        os.path.join(input_folder, f) for f in os.listdir(input_folder)
        if f.endswith('.png')
    ]
    pdf_files = [
        os.path.join(input_folder, f) for f in os.listdir(input_folder)
        if f.endswith('.pdf')
    ]

    tasks = []

    with ProcessPoolExecutor() as executor:
        # Submit tasks for PSD processing
        for psd_file in psd_files:
            tasks.append(executor.submit(process_psd, psd_file, temp_dir, dpi))

        # Submit tasks for PNG processing
        for png_file in png_files:
            tasks.append(
                executor.submit(process_png, png_file, temp_dir, verso_image,
                                split, dpi))

        # Submit tasks for copying PDFs
        for pdf_file in pdf_files:
            tasks.append(executor.submit(copy_pdf, pdf_file, temp_dir))

        # Use tqdm to track progress
        for future in tqdm(as_completed(tasks),
                           total=len(tasks),
                           desc="Processing files"):
            try:
                future.result()  # Ensure exceptions are raised if any
            except Exception as e:
                print(f"Error processing file: {e}")

    # Merge PDFs
    merge_pdfs(temp_dir, output_pdf)

    # Clean up temporary files
    shutil.rmtree(temp_dir)
